'use client';

import { useState, useEffect } from 'react';
import { TaskCard } from '@/components/TaskCard';
import { AddEditTaskModal } from '@/components/AddEditTaskModal';
import { EmptyState } from '@/components/EmptyState';
import { Button } from '@/components/ui/button';
import { PlusIcon } from 'lucide-react';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  createdAt: Date;
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Mock data for initial tasks
  useEffect(() => {
    const mockTasks: Task[] = [
      {
        id: 1,
        title: 'Complete project proposal',
        description: 'Finish the project proposal document and send to stakeholders',
        completed: false,
        priority: 'high',
        createdAt: new Date(),
      },
      {
        id: 2,
        title: 'Schedule team meeting',
        description: 'Arrange a meeting with the team for next week',
        completed: true,
        priority: 'medium',
        createdAt: new Date(Date.now() - 86400000), // 1 day ago
      },
    ];
    setTasks(mockTasks);
  }, []);

  const handleAddTask = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleDeleteTask = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleToggleComplete = (taskId: number) => {
    setTasks(tasks.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));
  };

  const handleSaveTask = (taskData: Omit<Task, 'id' | 'createdAt'> & { id?: number }) => {
    if (editingTask) {
      // Update existing task
      setTasks(tasks.map(task => 
        task.id === editingTask.id ? { ...task, ...taskData } as Task : task
      ));
    } else {
      // Add new task
      const newTask: Task = {
        ...taskData,
        id: Math.max(...tasks.map(t => t.id), 0) + 1,
        createdAt: new Date(),
      };
      setTasks([...tasks, newTask]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Tasks</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Manage your tasks efficiently
          </p>
        </header>

        <div className="flex justify-between items-center mb-6">
          <div className="relative w-64">
            <input
              type="text"
              placeholder="Search tasks..."
              className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <Button 
            onClick={handleAddTask}
            className="bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-2"
          >
            <PlusIcon className="w-4 h-4" />
            Add Task
          </Button>
        </div>

        {tasks.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={() => handleEditTask(task)}
                onDelete={() => handleDeleteTask(task.id)}
                onToggleComplete={() => handleToggleComplete(task.id)}
              />
            ))}
          </div>
        )}

        <AddEditTaskModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSaveTask}
          task={editingTask}
        />
      </div>
    </div>
  );
}