"use client";
import { Edit2, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { format } from "date-fns";
import { Badge } from "@/components/ui/badge";

export default function Task({ todo, onEdit, onDelete }) {
  const isoDate = todo.end_time;
  const formattedDate = format(new Date(isoDate), "MMMM d, yyyy, h:mm a");
  return (
    <div className="bg-card flex flex-col gap-4 min-h-14 max-w-96 p-4 rounded-md border-2">
      <div className="flex flex-row justify-between">
        <h2 className="text-xl font-bold mr-5 text-center">{todo.title}</h2>
        <Badge
          className="p-1 rounded-full"
          variant={todo.status === "urgent" ? "destructive" : "secondary"}
        >
          {todo.status}
        </Badge>
      </div>
      <div>{formattedDate}</div>
      <div>{todo.description}</div>
      <div className="flex flex-row">
        <Button variant="outline" size="icon" className="mr-5" onClick={onEdit}>
          <Edit2 />
        </Button>
        <Button variant="outline" size="icon" onClick={onDelete}>
          <Trash2 />
        </Button>
      </div>
    </div>
  );
}
