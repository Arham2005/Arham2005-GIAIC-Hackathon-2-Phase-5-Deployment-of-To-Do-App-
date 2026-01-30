'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { taskAPI } from '../../lib/api';
import { isAuthenticated, removeAuthToken } from '../../lib/auth';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { format } from 'date-fns';
import { CalendarIcon } from 'lucide-react';

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  user_id: number;
  created_at: string;
  priority?: string;
  tags?: string[];
  due_date?: string;
  recurring?: boolean;
  recurrence_pattern?: string;
  parent_task_id?: number;
  updated_at?: string;
  reminder_sent?: boolean;
}

const DashboardPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium',
    tags: [] as string[],
    due_date: '',
    recurring: false,
    recurrence_pattern: 'daily'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Delay the authentication check slightly to allow for token to be set
    const timer = setTimeout(() => {
      // Check if user is authenticated by checking for token in localStorage
      let token = null;
      if (typeof window !== 'undefined') {
        token = localStorage.getItem('auth_token');
      }

      console.log('Dashboard auth check - token exists:', !!token);

      if (!token) {
        console.log('No token found, redirecting to login');
        router.push('/login');
      } else {
        console.log('Token found, fetching tasks');
        fetchTasks();
      }
    }, 100); // Small delay to ensure token is available

    return () => clearTimeout(timer);
  }, []);

  const fetchTasks = async () => {
    try {
      const data = await taskAPI.getAll();
      setTasks(data);
      setError('');
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Prepare task data with advanced features
      const taskData: any = {
        title: newTask.title,
        description: newTask.description,
        priority: newTask.priority,
        tags: newTask.tags,
        recurring: newTask.recurring,
      };

      // Add due date if provided
      if (newTask.due_date) {
        taskData.due_date = new Date(newTask.due_date).toISOString();
      }

      // Add recurrence pattern if task is recurring
      if (newTask.recurring && newTask.recurrence_pattern) {
        taskData.recurrence_pattern = newTask.recurrence_pattern;
      }

      const task = await taskAPI.create(taskData);
      setTasks([...tasks, task]);
      setNewTask({
        title: '',
        description: '',
        priority: 'medium',
        tags: [],
        due_date: '',
        recurring: false,
        recurrence_pattern: 'daily'
      });
      setShowAdvancedOptions(false);
    } catch (err) {
      setError('Failed to add task');
      console.error('Error adding task:', err);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const updatedTask = await taskAPI.complete(taskId);
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await taskAPI.delete(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const handleLogout = () => {
    removeAuthToken();
    router.push('/login');
  };

  const handleTagChange = (tag: string) => {
    const newTags = newTask.tags.includes(tag)
      ? newTask.tags.filter(t => t !== tag)
      : [...newTask.tags, tag];
    setNewTask({...newTask, tags: newTags});
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600 mb-4"></div>
          <p className="text-gray-600">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  // Calculate statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const overdueTasks = tasks.filter(task =>
    !task.completed && task.due_date && new Date(task.due_date) < new Date()
  ).length;
  const highPriorityTasks = tasks.filter(task =>
    !task.completed && (task.priority === 'high' || task.priority === 'urgent')
  ).length;

  // Priority colors mapping
  const priorityColors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    urgent: 'bg-red-100 text-red-800'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-indigo-600">TodoPro Advanced</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-700">
                Welcome back! 👋
              </div>
              <button
                onClick={() => router.push('/tasks')}
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-200 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Advanced Tasks
              </button>
              <button
                onClick={() => router.push('/chat')}
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-200 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                AI Chat
              </button>
              <button
                onClick={fetchTasks}
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-green-600 hover:bg-green-700 transition-colors duration-200 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Refresh
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 rounded-md text-sm font-medium text-white bg-red-500 hover:bg-red-600 transition-colors duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Notification Banner */}
      <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 01-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-blue-700">
                <strong>Advanced Features:</strong> Create tasks with priorities, due dates, tags, and recurring options. Use the AI Chat to manage your tasks intelligently.
              </p>
            </div>
          </div>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl shadow-lg p-6 border border-blue-200">
            <div className="flex items-center">
              <div className="p-3 rounded-xl bg-blue-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-blue-600">Total Tasks</h3>
                <p className="text-3xl font-bold text-gray-900">{totalTasks}</p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl shadow-lg p-6 border border-green-200">
            <div className="flex items-center">
              <div className="p-3 rounded-xl bg-green-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-green-600">Completed</h3>
                <p className="text-3xl font-bold text-gray-900">{completedTasks}</p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-2xl shadow-lg p-6 border border-yellow-200">
            <div className="flex items-center">
              <div className="p-3 rounded-xl bg-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-yellow-600">Pending</h3>
                <p className="text-3xl font-bold text-gray-900">{pendingTasks}</p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-2xl shadow-lg p-6 border border-red-200">
            <div className="flex items-center">
              <div className="p-3 rounded-xl bg-red-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-red-600">Overdue</h3>
                <p className="text-3xl font-bold text-red-600">{overdueTasks}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Add Task Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Add New Task</h2>
                <button
                  onClick={() => setShowAdvancedOptions(!showAdvancedOptions)}
                  className="text-sm text-indigo-600 hover:text-indigo-800"
                >
                  {showAdvancedOptions ? 'Hide Advanced' : 'Show Advanced'}
                </button>
              </div>

              {error && (
                <div className="mb-4 rounded-md bg-red-50 p-3">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}

              <form onSubmit={handleAddTask} className="space-y-6">
                <div>
                  <label htmlFor="task-title" className="block text-sm font-medium text-gray-700 mb-2">
                    Task Title *
                  </label>
                  <input
                    type="text"
                    id="task-title"
                    value={newTask.title}
                    onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                    placeholder="What needs to be done?"
                    className="w-full px-4 py-3 text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="task-description" className="block text-sm font-medium text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    id="task-description"
                    value={newTask.description}
                    onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                    placeholder="Add details, context, or requirements..."
                    rows={4}
                    className="w-full px-4 py-3 text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                  />
                </div>

                <div className="pt-4 border-t border-gray-200">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-medium text-gray-900">Advanced Options</h3>
                    <button
                      type="button"
                      onClick={() => setShowAdvancedOptions(!showAdvancedOptions)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
                        showAdvancedOptions ? 'bg-indigo-600' : 'bg-gray-200'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          showAdvancedOptions ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>

                  {showAdvancedOptions && (
                    <div className="space-y-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Priority Level
                          </label>
                          <Select value={newTask.priority} onValueChange={(value) => setNewTask({...newTask, priority: value})}>
                            <SelectTrigger className="h-11">
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="low">
                                <div className="flex items-center">
                                  <div className="w-3 h-3 bg-green-400 rounded-full mr-2"></div>
                                  Low
                                </div>
                              </SelectItem>
                              <SelectItem value="medium">
                                <div className="flex items-center">
                                  <div className="w-3 h-3 bg-yellow-400 rounded-full mr-2"></div>
                                  Medium
                                </div>
                              </SelectItem>
                              <SelectItem value="high">
                                <div className="flex items-center">
                                  <div className="w-3 h-3 bg-orange-400 rounded-full mr-2"></div>
                                  High
                                </div>
                              </SelectItem>
                              <SelectItem value="urgent">
                                <div className="flex items-center">
                                  <div className="w-3 h-3 bg-red-400 rounded-full mr-2"></div>
                                  Urgent
                                </div>
                              </SelectItem>
                            </SelectContent>
                          </Select>
                        </div>

                        <div>
                          <label htmlFor="task-due-date" className="block text-sm font-medium text-gray-700 mb-2">
                            Due Date & Time
                          </label>
                          <input
                            type="datetime-local"
                            id="task-due-date"
                            value={newTask.due_date}
                            onChange={(e) => setNewTask({...newTask, due_date: e.target.value})}
                            className="w-full px-4 py-3 text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Tags
                        </label>
                        <div className="flex flex-wrap gap-2">
                          {['work', 'personal', 'important', 'meeting', 'follow-up', 'urgent', 'research', 'development'].map(tag => (
                            <button
                              key={tag}
                              type="button"
                              onClick={() => handleTagChange(tag)}
                              className={`px-3 py-1.5 text-sm rounded-full border transition-colors duration-200 ${
                                newTask.tags.includes(tag)
                                  ? 'bg-indigo-100 text-indigo-800 border-indigo-300 shadow-sm'
                                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                              }`}
                            >
                              #{tag}
                            </button>
                          ))}
                        </div>
                      </div>

                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-300">
                          <div className="flex items-center space-x-3">
                            <input
                              type="checkbox"
                              id="recurring"
                              checked={newTask.recurring}
                              onChange={(e) => setNewTask({...newTask, recurring: e.target.checked})}
                              className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500 border-gray-300"
                            />
                            <div>
                              <label htmlFor="recurring" className="text-sm font-medium text-gray-900">
                                Recurring Task
                              </label>
                              <p className="text-xs text-gray-500">Set up automatic repetition</p>
                            </div>
                          </div>
                        </div>

                        {newTask.recurring && (
                          <div className="ml-8">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Recurrence Pattern
                            </label>
                            <Select
                              value={newTask.recurrence_pattern}
                              onValueChange={(value) => setNewTask({...newTask, recurrence_pattern: value})}
                            >
                              <SelectTrigger className="h-11">
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="daily">Daily</SelectItem>
                                <SelectItem value="weekly">Weekly</SelectItem>
                                <SelectItem value="monthly">Monthly</SelectItem>
                                <SelectItem value="yearly">Yearly</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <button
                  type="submit"
                  className="w-full py-4 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold text-base rounded-lg shadow-lg transition-all duration-200 transform hover:scale-[1.02]"
                >
                  Add Task with Advanced Options
                </button>
              </form>
            </div>
          </div>

          {/* Right Column - Task List */}
          <div className="lg:col-span-2">
            <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-100 min-h-[500px]">
              <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-semibold text-gray-900">Your Tasks</h2>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-500">{tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}</span>
                  <div className="flex space-x-2">
                    <button
                      onClick={fetchTasks}
                      className="px-3 py-1.5 text-sm rounded-md text-gray-600 bg-gray-100 hover:bg-gray-200 transition-colors duration-200 flex items-center"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Refresh
                    </button>
                  </div>
                </div>
              </div>

              {tasks.length === 0 ? (
                <div className="text-center py-12">
                  <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-16 w-16 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <h3 className="mt-4 text-lg font-medium text-gray-900">No tasks yet</h3>
                  <p className="mt-2 text-sm text-gray-500">Get started by adding a new task with advanced features.</p>
                  <div className="mt-6">
                    <button
                      onClick={() => setShowAdvancedOptions(true)}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Enable Advanced Options
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-3">
                  {tasks.map((task) => (
                    <div
                      key={task.id}
                      className={`p-5 rounded-xl border transition-all duration-200 hover:shadow-md ${
                        task.completed
                          ? 'bg-green-50 border-green-200'
                          : task.due_date && new Date(task.due_date) < new Date() && !task.completed
                          ? 'bg-red-50 border-red-200 border-2'
                          : 'bg-white border-gray-200 hover:border-indigo-300'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-4 flex-1">
                          <div className="flex items-center h-5 mt-1">
                            <input
                              type="checkbox"
                              checked={task.completed}
                              onChange={() => handleToggleComplete(task.id)}
                              className="h-4 w-4 text-indigo-600 rounded focus:ring-indigo-500 border-gray-300"
                            />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center space-x-3 mb-2">
                              <h3 className={`font-semibold text-base ${
                                task.completed
                                  ? 'text-gray-500 line-through'
                                  : 'text-gray-900'
                              }`}>
                                {task.title}
                              </h3>
                              {task.priority && (
                                <Badge className={`${priorityColors[task.priority as keyof typeof priorityColors]} text-xs px-2 py-1`}>
                                  {task.priority.toUpperCase()}
                                </Badge>
                              )}
                              {task.recurring && (
                                <Badge variant="outline" className="text-xs px-2 py-1 bg-blue-50 border-blue-200 text-blue-700">
                                  🔁 {task.recurrence_pattern?.toUpperCase()}
                                </Badge>
                              )}
                            </div>

                            {task.description && (
                              <p className={`text-sm mb-3 ${
                                task.completed
                                  ? 'text-gray-400 line-through'
                                  : 'text-gray-600'
                              }`}>
                                {task.description}
                              </p>
                            )}

                            <div className="flex flex-wrap gap-2 mb-3">
                              {task.tags && task.tags.length > 0 && task.tags.map((tag, index) => (
                                <Badge key={index} variant="secondary" className="text-xs px-2 py-1 bg-indigo-100 text-indigo-700 border-indigo-200">
                                  #{tag}
                                </Badge>
                              ))}

                              {task.due_date && (
                                <Badge variant="outline" className="text-xs px-2 py-1 flex items-center gap-1">
                                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                  </svg>
                                  {format(new Date(task.due_date), 'MMM dd, yyyy HH:mm')}
                                </Badge>
                              )}
                            </div>

                            <div className="flex items-center justify-between text-xs text-gray-500">
                              <span>Created: {format(new Date(task.created_at), 'MMM dd, yyyy')}</span>
                              {task.updated_at && (
                                <span>Updated: {format(new Date(task.updated_at), 'MMM dd, yyyy')}</span>
                              )}
                            </div>
                          </div>
                        </div>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="text-gray-400 hover:text-red-500 transition-colors duration-200 p-1 hover:bg-red-50 rounded-md"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;