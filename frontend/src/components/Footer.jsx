// src/components/Footer.jsx

import React from 'react';

function Footer() {
  const currentYear = new Date().getFullYear();
  // You can pull the version from your package.json if you have a build process for it
  const appVersion = "1.0.0"; 

  return (
    <footer className="bg-gray-800 text-gray-400 shadow-inner">
      <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between sm:flex-row">
          <p className="text-sm">
            &copy; {currentYear} CodeIntel. All rights reserved.
          </p>
          <p className="mt-2 text-sm sm:mt-0">
            Version {appVersion}
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;