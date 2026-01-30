'use client';

import React, { useState, useEffect } from 'react';
import { taskAPI } from '../../lib/api';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { format } from 'date-fns';
import { PlusIcon, FilterIcon, CalendarIcon, FlagIcon, TagIcon, RepeatIcon } from 'lucide-react';

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: string;
  tags: string[];
  due_date?: string;
  recurring: boolean;
  recurrence_pattern?: string;
  parent_task_id?: number;
  created_at: string;
  updated_at?: string;
  reminder_sent?: boolean;
}

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentTask, setCurrentTask] = useState<Task | null>(null);
  const [filters, setFilters] = useState<any>({
    completed: null,
    priority: '',
    tags: [],
    due_date_from: '',
    due_date_to: '',
    search_query: '',
    sort_by: 'created_at',
    sort_order: 'asc'
  });

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [tasks, filters]);

  const fetchTasks = async () => {
    try {
      const data = await taskAPI.getAll();
      setTasks(data);
    } catch (err) {
      console.error('Error fetching tasks:', err);
    }
  };

  const applyFilters = () => {
    let filtered = [...tasks];

    if (filters.completed !== null && filters.completed !== undefined) {
      filtered = filtered.filter(task => task.completed === filters.completed);
    }

    if (filters.priority) {
      filtered = filtered.filter(task => task.priority === filters.priority);
    }

    if (filters.tags && filters.tags.length > 0) {
      filtered = filtered.filter(task =>
        filters.tags.some((tag: string) => task.tags.includes(tag))
      );
    }

    if (filters.search_query) {
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(filters.search_query.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(filters.search_query.toLowerCase()))
      );
    }

    if (filters.due_date_from) {
      filtered = filtered.filter(task =>
        task.due_date && new Date(task.due_date) >= new Date(filters.due_date_from)
      );
    }

    if (filters.due_date_to) {
      filtered = filtered.filter(task =>
        task.due_date && new Date(task.due_date) <= new Date(filters.due_date_to)
      );
    }

    // Apply sorting
    if (filters.sort_by) {
      filtered.sort((a, b) => {
        let aValue = a[filters.sort_by as keyof Task];
        let bValue = b[filters.sort_by as keyof Task];

        // Handle date comparisons
        if (filters.sort_by === 'due_date' || filters.sort_by === 'created_at') {
          aValue = aValue ? new Date(aValue as string).getTime() : 0;
          bValue = bValue ? new Date(bValue as string).getTime() : 0;
        }

        if (filters.sort_order === 'desc') {
          return (bValue as any) > (aValue as any) ? 1 : -1;
        } else {
          return (aValue as any) > (bValue as any) ? 1 : -1;
        }
      });
    }

    setFilteredTasks(filtered);
  };

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const updatedTask = await taskAPI.complete(taskId);
      setTasks(prev => prev.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  const handleEditTask = (task: Task) => {
    setCurrentTask(task);
    setIsModalOpen(true);
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await taskAPI.delete(taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const handleSubmitTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (currentTask) {
      try {
        if (currentTask.id) {
          // Update existing task
          const updatedTask = await taskAPI.update(currentTask.id, {
            title: currentTask.title,
            description: currentTask.description,
            completed: currentTask.completed,
            priority: currentTask.priority,
            tags: currentTask.tags,
            due_date: currentTask.due_date,
            recurring: currentTask.recurring,
            recurrence_pattern: currentTask.recurrence_pattern,
            parent_task_id: currentTask.parent_task_id,
            reminder_sent: currentTask.reminder_sent
          });

          setTasks(prev => prev.map(task =>
            task.id === currentTask.id ? updatedTask : task
          ));
        } else {
          // Create new task
          const newTask = await taskAPI.create({
            title: currentTask.title,
            description: currentTask.description,
            priority: currentTask.priority,
            tags: currentTask.tags,
            due_date: currentTask.due_date,
            recurring: currentTask.recurring,
            recurrence_pattern: currentTask.recurrence_pattern,
            parent_task_id: currentTask.parent_task_id
          });

          setTasks(prev => [...prev, newTask]);
        }

        setIsModalOpen(false);
        setCurrentTask(null);
      } catch (err) {
        console.error('Error saving task:', err);
      }
    }
  };

  const handleInputChange = (field: string, value: any) => {
    if (currentTask) {
      setCurrentTask({
        ...currentTask,
        [field]: value
      });
    }
  };

  const handleTagsChange = (tag: string, checked: boolean) => {
    if (currentTask) {
      const newTags = checked
        ? [...currentTask.tags, tag]
        : currentTask.tags.filter(t => t !== tag);

      setCurrentTask({
        ...currentTask,
        tags: newTags
      });
    }
  };

  const priorityColors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    urgent: 'bg-red-100 text-red-800'
  };

  const TaskCard = ({ task }: { task: Task }) => (
    <div className={`p-6 rounded-xl border transition-all duration-200 hover:shadow-md ${
      task.completed
        ? 'bg-green-50 border-green-200'
        : task.due_date && new Date(task.due_date) < new Date() && !task.completed
        ? 'bg-red-50 border-red-200 border-2'
        : 'bg-white border-gray-200 hover:border-indigo-300'
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-4 flex-1">
          <div className="flex items-center h-5 mt-1">
            <Checkbox
              checked={task.completed}
              onCheckedChange={() => handleToggleComplete(task.id)}
              className="h-4 w-4 text-indigo-600 rounded border-gray-300"
            />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-3 mb-3">
              <h3 className={`font-semibold text-lg ${
                task.completed
                  ? 'text-gray-500 line-through'
                  : 'text-gray-900'
              }`}>
                {task.title}
              </h3>
              {task.priority && (
                <Badge className={`${priorityColors[task.priority as keyof typeof priorityColors]} text-xs px-2 py-1`}>
                  <FlagIcon className="h-3 w-3 mr-1" />
                  {task.priority.toUpperCase()}
                </Badge>
              )}
            </div>

            {task.description && (
              <p className={`text-base mb-4 ${
                task.completed
                  ? 'text-gray-400 line-through'
                  : 'text-gray-600'
              }`}>
                {task.description}
              </p>
            )}

            <div className="flex flex-wrap gap-2 mb-4">
              {task.tags && task.tags.length > 0 && task.tags.map((tag, index) => (
                <Badge key={index} variant="secondary" className="text-xs px-2 py-1 bg-indigo-100 text-indigo-700 border-indigo-200">
                  <TagIcon className="h-3 w-3 mr-1" />
                  #{tag}
                </Badge>
              ))}

              {task.due_date && (
                <Badge variant="outline" className="text-xs px-2 py-1 flex items-center gap-1">
                  <CalendarIcon className="h-3 w-3" />
                  {format(new Date(task.due_date), 'MMM dd, yyyy HH:mm')}
                </Badge>
              )}

              {task.recurring && task.recurrence_pattern && (
                <Badge variant="outline" className="text-xs px-2 py-1 flex items-center gap-1 bg-blue-50 border-blue-200 text-blue-700">
                  <RepeatIcon className="h-3 w-3" />
                  {task.recurrence_pattern.toUpperCase()}
                </Badge>
              )}
            </div>

            <div className="flex items-center justify-between text-sm text-gray-500">
              <span>Created: {format(new Date(task.created_at), 'MMM dd, yyyy')}</span>
              {task.updated_at && (
                <span>Updated: {format(new Date(task.updated_at), 'MMM dd, yyyy')}</span>
              )}
            </div>
          </div>
        </div>
        <div className="flex space-x-2 ml-4">
          <Button variant="outline" size="sm" onClick={() => handleEditTask(task)} className="h-9 px-3">
            Edit
          </Button>
          <Button variant="outline" size="sm" onClick={() => handleDeleteTask(task.id)} className="h-9 px-3 text-red-600 hover:text-red-700 border-red-200 hover:border-red-300">
            Delete
          </Button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8 border border-indigo-100">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Advanced Task Management</h1>
          <p className="text-lg text-gray-600">Manage tasks with priorities, tags, due dates, and recurrence patterns</p>
          <div className="mt-4 flex items-center space-x-6 text-sm text-gray-500">
            <div className="flex items-center">
              <FlagIcon className="h-4 w-4 mr-2 text-indigo-500" />
              Priority levels (Low/Medium/High/Urgent)
            </div>
            <div className="flex items-center">
              <TagIcon className="h-4 w-4 mr-2 text-indigo-500" />
              Custom tags for organization
            </div>
            <div className="flex items-center">
              <CalendarIcon className="h-4 w-4 mr-2 text-indigo-500" />
              Due dates and time scheduling
            </div>
            <div className="flex items-center">
              <RepeatIcon className="h-4 w-4 mr-2 text-indigo-500" />
              Recurring task patterns
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center mb-6">
        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setCurrentTask({
              id: 0,
              title: '',
              description: '',
              completed: false,
              priority: 'medium',
              tags: [],
              due_date: '',
              recurring: false,
              recurrence_pattern: 'daily',
              parent_task_id: undefined,
              created_at: new Date().toISOString(),
              updated_at: undefined,
              reminder_sent: false
            })} className="h-12 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold">
              <PlusIcon className="mr-2 h-5 w-5" />
              Add New Task
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{currentTask?.id ? 'Edit Task' : 'Create New Task'}</DialogTitle>
            </DialogHeader>

            <form onSubmit={handleSubmitTask}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Title *</Label>
                  <Input
                    id="title"
                    value={currentTask?.title || ''}
                    onChange={(e) => handleInputChange('title', e.target.value)}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="priority">Priority</Label>
                  <Select
                    value={currentTask?.priority || 'medium'}
                    onValueChange={(value) => handleInputChange('priority', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="urgent">Urgent</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={currentTask?.description || ''}
                    onChange={(e) => handleInputChange('description', e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="due_date">Due Date</Label>
                  <Input
                    id="due_date"
                    type="datetime-local"
                    value={currentTask?.due_date ? currentTask.due_date.substring(0, 16) : ''}
                    onChange={(e) => handleInputChange('due_date', e.target.value + ':00Z')}
                  />
                </div>

                <div className="space-y-2">
                  <Label>Tags</Label>
                  <div className="flex flex-wrap gap-2">
                    {['work', 'personal', 'important', 'meeting', 'follow-up'].map(tag => (
                      <div key={tag} className="flex items-center space-x-2">
                        <Checkbox
                          id={tag}
                          checked={currentTask?.tags.includes(tag) || false}
                          onCheckedChange={(checked) => handleTagsChange(tag, checked as boolean)}
                        />
                        <Label htmlFor={tag} className="text-sm">{tag}</Label>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="recurring"
                      checked={currentTask?.recurring || false}
                      onCheckedChange={(checked) => handleInputChange('recurring', checked)}
                    />
                    <Label htmlFor="recurring">Recurring Task</Label>
                  </div>

                  {currentTask?.recurring && (
                    <Select
                      value={currentTask?.recurrence_pattern || 'daily'}
                      onValueChange={(value) => handleInputChange('recurrence_pattern', value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="daily">Daily</SelectItem>
                        <SelectItem value="weekly">Weekly</SelectItem>
                        <SelectItem value="monthly">Monthly</SelectItem>
                        <SelectItem value="yearly">Yearly</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                </div>
              </div>

              <div className="flex justify-end space-x-2 mt-6">
                <Button type="button" variant="outline" onClick={() => setIsModalOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit">
                  {currentTask?.id ? 'Update Task' : 'Create Task'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="space-y-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Priority Filter */}
          <div>
            <Label>Priority</Label>
            <Select
              value={filters.priority}
              onValueChange={(value) => handleFilterChange('priority', value)}
            >
              <SelectTrigger>
                <SelectValue placeholder="All Priorities" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Priorities</SelectItem>
                <SelectItem value="low">Low</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="urgent">Urgent</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Completion Status */}
          <div>
            <Label>Status</Label>
            <Select
              value={filters.completed === null ? '' : filters.completed.toString()}
              onValueChange={(value) => handleFilterChange('completed', value === '' ? null : value === 'true')}
            >
              <SelectTrigger>
                <SelectValue placeholder="All Statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Statuses</SelectItem>
                <SelectItem value="false">Pending</SelectItem>
                <SelectItem value="true">Completed</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Sort By */}
          <div>
            <Label>Sort By</Label>
            <Select
              value={filters.sort_by}
              onValueChange={(value) => handleFilterChange('sort_by', value)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="created_at">Created Date</SelectItem>
                <SelectItem value="due_date">Due Date</SelectItem>
                <SelectItem value="priority">Priority</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Sort Order */}
          <div>
            <Label>Order</Label>
            <Select
              value={filters.sort_order}
              onValueChange={(value) => handleFilterChange('sort_order', value)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="asc">Ascending</SelectItem>
                <SelectItem value="desc">Descending</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label>Due Date From</Label>
            <Input
              type="datetime-local"
              value={filters.due_date_from}
              onChange={(e) => handleFilterChange('due_date_from', e.target.value)}
            />
          </div>

          <div>
            <Label>Due Date To</Label>
            <Input
              type="datetime-local"
              value={filters.due_date_to}
              onChange={(e) => handleFilterChange('due_date_to', e.target.value)}
            />
          </div>
        </div>

        <div>
          <Label>Search</Label>
          <Input
            placeholder="Search tasks..."
            value={filters.search_query}
            onChange={(e) => handleFilterChange('search_query', e.target.value)}
          />
        </div>
      </div>

      <div className="mt-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-6 border border-indigo-100 min-h-[500px]">
        <Tabs defaultValue="all" className="w-full">
          <TabsList className="grid w-full grid-cols-3 bg-white border border-gray-200 rounded-xl p-1 shadow-sm">
            <TabsTrigger value="all" className="data-[state=active]:bg-indigo-500 data-[state=active]:text-white rounded-lg">All Tasks</TabsTrigger>
            <TabsTrigger value="pending" className="data-[state=active]:bg-indigo-500 data-[state=active]:text-white rounded-lg">Pending</TabsTrigger>
            <TabsTrigger value="completed" className="data-[state=active]:bg-indigo-500 data-[state=active]:text-white rounded-lg">Completed</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="mt-6">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">All Tasks</h3>
              {filteredTasks.length === 0 ? (
                <div className="text-center py-12">
                  <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-16 w-16 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <h3 className="mt-4 text-lg font-medium text-gray-900">No tasks yet</h3>
                  <p className="mt-2 text-sm text-gray-500">Get started by adding a new task with advanced features.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredTasks.map(task => (
                    <TaskCard key={task.id} task={task} />
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="pending" className="mt-6">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Pending Tasks</h3>
              {filteredTasks.filter(t => !t.completed).length === 0 ? (
                <div className="text-center py-12">
                  <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-16 w-16 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <h3 className="mt-4 text-lg font-medium text-gray-900">No pending tasks</h3>
                  <p className="mt-2 text-sm text-gray-500">All tasks are completed!</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredTasks.filter(t => !t.completed).map(task => (
                    <TaskCard key={task.id} task={task} />
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="completed" className="mt-6">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Completed Tasks</h3>
              {filteredTasks.filter(t => t.completed).length === 0 ? (
                <div className="text-center py-12">
                  <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-16 w-16 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <h3 className="mt-4 text-lg font-medium text-gray-900">No completed tasks</h3>
                  <p className="mt-2 text-sm text-gray-500">Start completing tasks to see them here.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredTasks.filter(t => t.completed).map(task => (
                    <TaskCard key={task.id} task={task} />
                  ))}
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default TasksPage;