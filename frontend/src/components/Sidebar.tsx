import { NavLink } from "react-router-dom";
 
const NAV_ITEMS = [
  { to: "/", label: "Dashboard" },
  { to: "/agente", label: "Agente" },
];
 
export function Sidebar() {
  return (
    <aside className="flex h-screen w-60 flex-col border-r border-white/5 bg-surface px-4 py-6">
      <div className="mb-8 px-2">
        <span className="font-display text-sm font-semibold text-white">
          Agentic RAG
        </span>
      </div>
 
      <nav className="flex flex-col gap-1">
        {NAV_ITEMS.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            end
            className={({ isActive }) =>
              [
                "rounded-lg px-3 py-2 text-sm transition",
                isActive ? "bg-white/5 text-white" : "text-muted hover:bg-white/5",
              ].join(" ")
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
