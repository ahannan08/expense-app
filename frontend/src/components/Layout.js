import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './styles/Layout.css';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/prediction', label: 'Predict' },
  { to: '/log-expense', label: 'Log expense' },
  { to: '/expenses', label: 'Expenses' },
  { to: '/summary', label: 'Summary' },
];

function Layout({ children, title, subtitle }) {
  const { pathname } = useLocation();

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-inner">
          <Link to="/" className="app-brand">
            Expense<span>Predict</span>
          </Link>
          <nav className="app-nav" aria-label="Main">
            {navItems.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className={`app-nav-link${pathname === to ? ' active' : ''}`}
              >
                {label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="app-main">
        {(title || subtitle) && (
          <div className="page-heading">
            {title && <h1>{title}</h1>}
            {subtitle && <p className="page-subtitle">{subtitle}</p>}
          </div>
        )}
        {children}
      </main>
    </div>
  );
}

export default Layout;
