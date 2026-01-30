'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import TaskFilters from './components/TaskFilters';
import TaskCard from './components/TaskCard';
import { PlusIcon, FilterIcon } from 'lucide-react';

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
}

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentTask, setCurrentTask] = useState<Task | null>(null);
  const [filters, setFilters] = useState<any>({});

  // Mock data for initial tasks
  useEffect(() => {
    const mockTasks: Task[] = [
      {
        id: 1,
        title: 'Complete project proposal',
        description: 'Finish the project proposal document for client review',
        completed: false,
        priority: 'high',
        tags: ['work', 'important'],
        due_date: '2024-02-15T10:00:00Z',
        recurring: false,
        recurrence_pattern: '',
        created_at: '2024-01-30T09:00:00Z',
      },
      {
        id: 2,
        title: 'Team meeting',
        description: 'Weekly team sync meeting',
        completed: false,
        priority: 'medium',
        tags: ['meeting', 'team'],
        due_date: '2024-02-01T14:00:00Z',
        recurring: true,
        recurrence_pattern: 'weekly',
        created_at: '2024-01-29T15:00:00Z',
      },
      {
        id: 3,
        title: 'Buy groceries',
        description: 'Milk, eggs, bread, fruits',
        completed: true,
        priority: 'low',
        tags: ['personal'],
        due_date: '2024-01-31T18:00:00Z',
        recurring: false,
        recurrence_pattern: '',
        created_at: '2024-01-28T08:00:00Z',
      },
      {
        id: 4,
        title: 'Review code changes',
        description: 'Review pull request from John',
        completed: false,
        priority: 'urgent',
        tags: ['work', 'code-review'],
        due_date: '2024-02-02T12:00:00Z',
        recurring: false,
        recurrence_pattern: '',
        created_at: '2024-01-30T10:30:00Z',
      }
    ];

    setTasks(mockTasks);
    setFilteredTasks(mockTasks);
  }, []);

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);

    // Apply filters to tasks
    let filtered = [...tasks];

    if (newFilters.completed !== null && newFilters.completed !== undefined) {
      filtered = filtered.filter(task => task.completed === newFilters.completed);
    }

    if (newFilters.priority) {
      filtered = filtered.filter(task => task.priority === newFilters.priority);
    }

    if (newFilters.tags && newFilters.tags.length > 0) {
      filtered = filtered.filter(task =>
        newFilters.tags.some((tag: string) => task.tags.includes(tag))
      );
    }

    if (newFilters.search_query) {
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(newFilters.search_query.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(newFilters.search_query.toLowerCase()))
      );
    }

    if (newFilters.due_date_from) {
      filtered = filtered.filter(task =>
        task.due_date && new Date(task.due_date) >= new Date(newFilters.due_date_from)
      );
    }

    if (newFilters.due_date_to) {
      filtered = filtered.filter(task =>
        task.due_date && new Date(task.due_date) <= new Date(newFilters.due_date_to)
      );
    }

    // Apply sorting
    if (newFilters.sort_by) {
      filtered.sort((a, b) => {
        let aValue = a[newFilters.sort_by as keyof Task];
        let bValue = b[newFilters.sort_by as keyof Task];

        // Handle date comparisons
        if (newFilters.sort_by === 'due_date' || newFilters.sort_by === 'created_at') {
          aValue = aValue ? new Date(aValue as string).getTime() : 0;
          bValue = bValue ? new Date(bValue as string).getTime() : 0;
        }

        if (newFilters.sort_order === 'desc') {
          return (bValue as any) > (aValue as any) ? 1 : -1;
        } else {
          return (aValue as any) > (bValue as any) ? 1 : -1;
        }
      });
    }

    setFilteredTasks(filtered);
  };

  const handleToggleComplete = (taskId: number) => {
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      )
    );

    setFilteredTasks(prevFiltered =>
      prevFiltered.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      )
    );
  };

  const handleEditTask = (taskId: number) => {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      setCurrentTask(task);
      setIsModalOpen(true);
    }
  };

  const handleDeleteTask = (taskId: number) => {
    setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
    setFilteredTasks(prevFiltered => prevFiltered.filter(task => task.id !== taskId));
  };

  const handleSubmitTask = (e: React.FormEvent) => {
    e.preventDefault();

    if (currentTask) {
      // In a real app, this would call an API
      if (currentTask.id) {
        // Update existing task
        setTasks(prev =>
          prev.map(task => task.id === currentTask.id ? currentTask : task)
        );
      } else {
        // Create new task
        const newTask = {
          ...currentTask,
          id: Math.max(...prev.map(t => t.id), 0) + 1, // Simple ID generation
          created_at: new Date().toISOString()
        };
        setTasks(prev => [...prev, newTask]);
      }

      // Close modal and reset form
      setIsModalOpen(false);
      setCurrentTask(null);
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

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Advanced Task Management</h1>
        <p className="text-gray-600 mt-2">Manage tasks with priorities, tags, due dates, and recurrence</p>
      </div>

      <div className="flex justify-between items-center mb-6">
        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setCurrentTask(null)}>
              <PlusIcon className="mr-2 h-4 w-4" />
              Add Task
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{currentTask ? 'Edit Task' : 'Create New Task'}</DialogTitle>
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
                  {currentTask ? 'Update Task' : 'Create Task'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <TaskFilters onFilterChange={handleFilterChange} />

      <div className="mt-6">
        <Tabs defaultValue="all" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="all">All Tasks</TabsTrigger>
            <TabsTrigger value="pending">Pending</TabsTrigger>
            <TabsTrigger value="completed">Completed</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="mt-4">
            {filteredTasks.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                No tasks found. Create a new task to get started.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredTasks.map(task => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onToggleComplete={handleToggleComplete}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                  />
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="pending" className="mt-4">
            {filteredTasks.filter(t => !t.completed).length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                No pending tasks found.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredTasks.filter(t => !t.completed).map(task => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onToggleComplete={handleToggleComplete}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                  />
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="completed" className="mt-4">
            {filteredTasks.filter(t => t.completed).length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                No completed tasks found.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredTasks.filter(t => t.completed).map(task => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onToggleComplete={handleToggleComplete}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                  />
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default TasksPage;