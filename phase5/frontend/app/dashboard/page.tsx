'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { CalendarIcon, ClockIcon, FlagIcon, RepeatIcon, TrendingUpIcon, CheckCircleIcon } from 'lucide-react';
import { format, addDays } from 'date-fns';

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
  created_at: string;
  updated_at?: string;
}

const DashboardPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    pending: 0,
    overdue: 0,
    highPriority: 0
  });

  // Mock data for tasks
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
      },
      {
        id: 5,
        title: 'Gym workout',
        description: 'Cardio and strength training',
        completed: false,
        priority: 'medium',
        tags: ['fitness', 'health'],
        due_date: '2024-01-31T19:00:00Z',
        recurring: true,
        recurrence_pattern: 'daily',
        created_at: '2024-01-25T07:00:00Z',
      }
    ];

    setTasks(mockTasks);

    // Calculate stats
    const total = mockTasks.length;
    const completed = mockTasks.filter(t => t.completed).length;
    const pending = total - completed;
    const overdue = mockTasks.filter(t =>
      !t.completed && t.due_date && new Date(t.due_date) < new Date()
    ).length;
    const highPriority = mockTasks.filter(t =>
      !t.completed && (t.priority === 'high' || t.priority === 'urgent')
    ).length;

    setStats({ total, completed, pending, overdue, highPriority });
  }, []);

  const priorityColors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    urgent: 'bg-red-100 text-red-800'
  };

  const upcomingTasks = tasks
    .filter(task => !task.completed && task.due_date)
    .sort((a, b) => new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime())
    .slice(0, 5);

  const recurringTasks = tasks.filter(task => task.recurring).slice(0, 3);

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back! Here's what you need to focus on today.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
            <TrendingUpIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <CheckCircleIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completed}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending</CardTitle>
            <ClockIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pending}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Overdue</CardTitle>
            <CalendarIcon className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">{stats.overdue}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">High Priority</CardTitle>
            <FlagIcon className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-500">{stats.highPriority}</div>
          </CardContent>
        </Card>
      </div>

      {/* Progress Bar */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Task Progress</CardTitle>
          <CardDescription>Your completion rate</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-2">
            <span>Progress</span>
            <span>{stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0}%</span>
          </div>
          <Progress value={stats.total > 0 ? (stats.completed / stats.total) * 100 : 0} className="h-2" />
        </CardContent>
      </Card>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upcoming Tasks */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Upcoming Tasks</CardTitle>
            <CardDescription>Your next 5 tasks</CardDescription>
          </CardHeader>
          <CardContent>
            {upcomingTasks.length > 0 ? (
              <div className="space-y-4">
                {upcomingTasks.map(task => (
                  <div key={task.id} className="flex items-start space-x-4 p-3 border rounded-lg hover:bg-gray-50">
                    <div className="flex-1">
                      <h4 className="font-medium">{task.title}</h4>
                      <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                      <div className="flex items-center mt-2 space-x-2">
                        <Badge className={priorityColors[task.priority as keyof typeof priorityColors]}>
                          {task.priority}
                        </Badge>
                        {task.due_date && (
                          <div className="flex items-center text-sm text-gray-500">
                            <CalendarIcon className="h-4 w-4 mr-1" />
                            {format(new Date(task.due_date), 'MMM dd, yyyy HH:mm')}
                          </div>
                        )}
                      </div>
                    </div>
                    <Link href={`/tasks/${task.id}`}>
                      <Button variant="outline" size="sm">View</Button>
                    </Link>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No upcoming tasks</p>
            )}
          </CardContent>
        </Card>

        {/* Recurring Tasks */}
        <Card>
          <CardHeader>
            <CardTitle>Recurring Tasks</CardTitle>
            <CardDescription>Tasks that repeat</CardDescription>
          </CardHeader>
          <CardContent>
            {recurringTasks.length > 0 ? (
              <div className="space-y-4">
                {recurringTasks.map(task => (
                  <div key={task.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <h4 className="font-medium">{task.title}</h4>
                      <div className="flex items-center text-sm text-gray-500 mt-1">
                        <RepeatIcon className="h-4 w-4 mr-1" />
                        {task.recurrence_pattern}
                      </div>
                    </div>
                    <Badge variant="outline">{task.tags[0]}</Badge>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No recurring tasks</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Priority Tasks */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>High Priority Tasks</CardTitle>
          <CardDescription>Tasks requiring immediate attention</CardDescription>
        </CardHeader>
        <CardContent>
          {tasks.filter(t => !t.completed && (t.priority === 'high' || t.priority === 'urgent')).length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tasks
                .filter(task => !task.completed && (task.priority === 'high' || task.priority === 'urgent'))
                .map(task => (
                  <div key={task.id} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start">
                      <h4 className="font-medium">{task.title}</h4>
                      <Badge className={priorityColors[task.priority as keyof typeof priorityColors]}>
                        {task.priority}
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">{task.description}</p>
                    {task.due_date && (
                      <div className="flex items-center mt-2 text-sm text-red-600">
                        <CalendarIcon className="h-4 w-4 mr-1" />
                        Due: {format(new Date(task.due_date), 'MMM dd, yyyy HH:mm')}
                      </div>
                    )}
                    <div className="flex justify-between items-center mt-3">
                      <div className="flex gap-1">
                        {task.tags.slice(0, 2).map((tag, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                      <Link href={`/tasks/${task.id}`}>
                        <Button variant="outline" size="sm">Details</Button>
                      </Link>
                    </div>
                  </div>
                ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">No high priority tasks</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardPage;