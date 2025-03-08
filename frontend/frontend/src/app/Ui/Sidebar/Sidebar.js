"use client";
import { useState } from "react";
import { ThemeToggle } from "@/app/ThemeToggle";
import { Button } from "@/components/ui/button";
import { Menu, X, PlusCircle, LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

export default function Sidebar({ children }) {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const logout = () => {
    sessionStorage.removeItem("token");
    router.push('/login');
  };
  return (
    <div className="flex min-h-screen">
      <button
        className="p-2 md:hidden fixed top-2 left-2 bg-card rounded text-foreground z-50 block"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <X /> : <Menu />}
      </button>

      {/* Sidebar */}
      <aside
        className={`h-screen w-64 bg-card p-4 fixed md:static transition-transform duration-300 z-40 
          ${isOpen ? "translate-x-0" : "-translate-x-full"} 
          md:translate-x-0 border-r-2`}
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Task Manager</h2>
          <ThemeToggle />
        </div>
        <nav className="space-y-4">
          <Button variant="ghost" className="w-full justify-start">
            <PlusCircle className="mr-2" />
            New Task
          </Button>
        </nav>
        <nav className="space-y-4">
          <Button variant="ghost" className="w-full justify-start" onClick={logout}>
            <LogOut className="mr-2" />
            Logout
          </Button>
        </nav>
      </aside>

      {/* Main Content (takes remaining space) */}
      <main className="flex-1 p-4 md:ml-8">{children}</main>
    </div>
  );
}
