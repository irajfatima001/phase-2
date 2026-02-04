import { Task } from '@/app/dashboard/page';
import { toast } from 'sonner';

// This would typically be a Redux, Zustand, or React Context implementation
// For this example, I'll create a simple module-level state management

let tasks: Task[] = [];
let listeners: Array<() => void> = [];

const taskStore = {
  subscribe: (listener: () => void) => {
    listeners.push(listener);
    return () => {
      listeners = listeners.filter(l => l !== listener);
    };
  },

  getTasks: (): Task[] => tasks,

  setTasks: (newTasks: Task[]) => {
    tasks = [...newTasks];
    listeners.forEach(listener => listener());
  },

  addTask: (task: Omit<Task, 'id' | 'createdAt'>) => {
    const newTask: Task = {
      ...task,
      id: Math.max(0, ...tasks.map(t => t.id)) + 1,
      createdAt: new Date(),
    };
    
    tasks = [...tasks, newTask];
    listeners.forEach(listener => listener());
    toast.success('Task added successfully!');
  },

  updateTask: (updatedTask: Task) => {
    tasks = tasks.map(task => 
      task.id === updatedTask.id ? updatedTask : task
    );
    listeners.forEach(listener => listener());
    toast.success('Task updated successfully!');
  },

  deleteTask: (taskId: number) => {
    tasks = tasks.filter(task => task.id !== taskId);
    listeners.forEach(listener => listener());
    toast.success('Task deleted successfully!');
  },

  toggleTaskCompletion: (taskId: number) => {
    tasks = tasks.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    );
    listeners.forEach(listener => listener());
    
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      toast.success(`Task marked as ${task.completed ? 'incomplete' : 'complete'}!`);
    }
  },
};

export default taskStore;