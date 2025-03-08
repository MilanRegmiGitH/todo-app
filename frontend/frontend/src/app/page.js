"use client";
import Link from "next/link";
import Task from "./Ui/Task/Task";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_PATH } from "@/lib/apipath";
import { toast } from "sonner";
import SideBar from "./Ui/Sidebar/Sidebar";

export default function App() {
  const [token, setToken] = useState("");
  const [tasks, setTasks] = useState([]);
  const router = useRouter();

  const deleteTask = async (id) => {
    try {
      await axios.delete(`${API_PATH.DELETE.DELETE_TASK}/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTasks(tasks.filter((task) => task.id !== id));
      toast.success("Task deleted successfully");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to delete task");
    }
  };

  useEffect(() => {
    const fetchTasks = async () => {
      const access_token = sessionStorage.getItem("token");
      console.log(access_token);
      if (!access_token) {
        router.push("/login");
        return;
      }
      setToken(access_token);

      try {
        const response = await axios.get(API_PATH.GET.GET_TASKS, {
          headers: { Authorization: `Bearer ${access_token}` },
        });
        if (!response.data) {
          throw new Error("Tasks could not be retrieved");
        }
        console.log(response.data);
        setTasks(response.data);
      } catch (err) {
        router.push("/login");
        toast.error(
          err.response?.data?.detail || "Tasks could not be retrieved."
        );
      }
    };

    fetchTasks();
  }, [router]);

  return (
    <div className="min-h-screen">
      <SideBar>
        {tasks.length == 0 ? <h1 className="text-center text-3xl font-bold text-accent mt-5">Start by adding some tasks</h1>:""}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 mt-5">
          {tasks.map((task) => (
            <Task key={task.id} todo={task} onDelete={()=>deleteTask(task.id)}></Task>
          ))}
        </div>
      </SideBar>
    </div>
  );
}
