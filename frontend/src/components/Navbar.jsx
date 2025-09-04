// src/components/Navbar.jsx

import React, { useState } from 'react';

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  // A simple link component for styling consistency
  const NavLink = ({ href, children }) => (
    <a
      href={href}
      className="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white md:inline-block md:px-0 md:py-0 md:hover:bg-transparent md:hover:text-cyan-400"
    >
      {children}
    </a>
  );

  return (
    <nav className="bg-gray-800 shadow-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo/Brand */}
          <div className="flex-shrink-0">
            <a href="/" className="text-2xl font-bold text-white">
              Code<span className="text-cyan-400">Intel</span>
            </a>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <NavLink href="/">Home</NavLink>
              <NavLink href="/ingest">Ingest</NavLink>
              <NavLink href="/query">Query</NavLink>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="-mr-2 flex md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              type="button"
              className="inline-flex items-center justify-center rounded-md bg-gray-700 p-2 text-gray-400 hover:bg-gray-600 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
              aria-controls="mobile-menu"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {/* Icon for menu open/close */}
              <svg
                className={`${isOpen ? 'hidden' : 'block'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg
                className={`${isOpen ? 'block' : 'hidden'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu, show/hide based on state */}
      <div className={`${isOpen ? 'block' : 'hidden'} md:hidden`} id="mobile-menu">
        <div className="space-y-1 px-2 pb-3 pt-2 sm:px-3">
          <NavLink href="/">Home</NavLink>
          <NavLink href="/ingest">Ingest</NavLink>
          <NavLink href="/query">Query</NavLink>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
