import { BrowserRouter, Route, Routes } from "react-router-dom";
 
import { AppLayout } from "./components/AppLayout";
import { Agent } from "./pages/Agent";
import { Dashboard } from "./pages/Dashboard";
 
export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="agente" element={<Agent />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
