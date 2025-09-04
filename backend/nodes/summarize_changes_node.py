# backend/nodes/summarize_changes_node.py

import asyncio
import time
from typing import List, Dict, Any, Union

# --- LangChain and LLM Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .change_detection_node import GraphState, ChangedItem
from ..summarizer.models import FunctionSummary, ClassSummary, MethodSummary
from ..parser.parser import parse_file

# --- Configuration for Rate Limiting ---
# Delay in seconds between each API call to avoid hitting rate limits.
# A value of 1.1 means we are making slightly less than 60 calls per minute.
API_CALL_DELAY = 1.1

# --- Real LLM Utility ---
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert code assistant. Summarize the following code snippet in 1-2 concise sentences, explaining its primary purpose and functionality."),
    ("human", "Code snippet:\n\n```python\n{code_snippet}\n```"),
])
summarizer_chain = prompt | llm | StrOutputParser()

async def summarize_code_with_llm(code: str) -> str:
    """
    Asynchronously invokes the LLM chain to get a summary for a single block of code.
    Includes a delay to manage API rate limits.
    """
    try:
        summary = await summarizer_chain.ainvoke({"code_snippet": code})
        await asyncio.sleep(API_CALL_DELAY)
        return summary
    except Exception as e:
        print(f"LLM call failed: {e}")
        await asyncio.sleep(API_CALL_DELAY)
        return "Error: Could not generate summary."

# --- The LangGraph Node (Now fully asynchronous) ---
async def summarize_changes_node(state: GraphState) -> Dict[str, List]:
    """
    An async LangGraph node that processes a list of changed code items and generates summaries.
    """
    print("--- Summarization Node Triggered ---")
    changes = state.get("changes", [])
    tasks = []

    changes_by_file: Dict[str, List[ChangedItem]] = {}
    for change in changes:
        if change.file_path not in changes_by_file:
            changes_by_file[change.file_path] = []
        changes_by_file[change.file_path].append(change)

    for file_path, file_changes in changes_by_file.items():
        items_to_summarize = [c for c in file_changes if c.change_type in ('added', 'modified')]
        if not items_to_summarize:
            continue

        try:
            parsed_result = parse_file(file_path)
            for change in items_to_summarize:
                if change.item_type == 'function':
                    item = next((f for f in parsed_result.functions if f.name == change.item_name), None)
                    if item: tasks.append(create_summary_task(item, file_path, 'function'))
                
                elif change.item_type == 'class':
                    item = next((c for c in parsed_result.classes if c.name == change.item_name), None)
                    if item: tasks.append(create_summary_task(item, file_path, 'class'))

                elif change.item_type == 'method':
                    for cls in parsed_result.classes:
                        item = next((m for m in cls.methods if m.name == change.item_name), None)
                        if item:
                            tasks.append(create_summary_task(item, file_path, 'method', cls.name))
                            break
        except Exception as e:
            print(f"Error while preparing summaries for {file_path}: {e}")

    summaries = []
    if tasks:
        # Run all summarization tasks concurrently
        summaries = await asyncio.gather(*tasks)
    
    print(f"Generated {len(summaries)} new/updated summaries.")
    return {"summaries": summaries}


async def create_summary_task(item: Any, file_path: str, item_type: str, class_name: str = None):
    """Helper function to create a specific summary object after LLM call."""
    summary_text = await summarize_code_with_llm(item.source_code)
    if item_type == 'function':
        return FunctionSummary(file_path=file_path, function_name=item.name, summary=summary_text)
    elif item_type == 'class':
        return ClassSummary(file_path=file_path, class_name=item.name, summary=summary_text)
    elif item_type == 'method':
        return MethodSummary(file_path=file_path, class_name=class_name, method_name=item.name, summary=summary_text)
