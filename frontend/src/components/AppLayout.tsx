import { Outlet } from "react-router-dom";
 
import { Sidebar } from "./Sidebar";
 
export function AppLayout() {
  return (
    <div className="flex min-h-screen bg-ink text-white">
      <Sidebar />
      <div className="flex-1 overflow-y-auto">
        <Outlet />
      </div>
    </div>
  );
}
