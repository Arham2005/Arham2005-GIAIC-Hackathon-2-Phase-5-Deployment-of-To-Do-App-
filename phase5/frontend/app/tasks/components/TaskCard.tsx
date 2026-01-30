'use client';

import React from 'react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import {
  CalendarIcon,
  ClockIcon,
  RepeatIcon,
  FlagIcon,
  TagIcon,
  MoreHorizontalIcon
} from 'lucide-react';
import { format } from 'date-fns';

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

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}

const TaskCard = ({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) => {
  const priorityColors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    urgent: 'bg-red-100 text-red-800'
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    return format(new Date(dateString), 'MMM dd, yyyy');
  };

  const formatTime = (dateString?: string) => {
    if (!dateString) return '';
    return format(new Date(dateString), 'HH:mm');
  };

  return (
    <Card className={`transition-all hover:shadow-md ${task.completed ? 'opacity-75' : ''}`}>
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <Checkbox
              checked={task.completed}
              onCheckedChange={() => onToggleComplete(task.id)}
              className="mt-1"
            />
            <div className="flex-1">
              <h3 className={`font-semibold ${task.completed ? 'line-through' : ''}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className="text-sm text-gray-600 mt-1">{task.description}</p>
              )}
            </div>
          </div>
          <Button variant="ghost" size="sm" onClick={() => onEdit(task.id)}>
            <MoreHorizontalIcon className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>

      <CardContent className="pb-2">
        <div className="flex flex-wrap items-center gap-2 mb-2">
          <Badge className={priorityColors[task.priority as keyof typeof priorityColors]}>
            <FlagIcon className="h-3 w-3 mr-1" />
            {task.priority}
          </Badge>

          {task.due_date && (
            <div className="flex items-center text-sm text-gray-600">
              <CalendarIcon className="h-4 w-4 mr-1" />
              {formatDate(task.due_date)} {formatTime(task.due_date)}
            </div>
          )}

          {task.recurring && task.recurrence_pattern && (
            <div className="flex items-center text-sm text-blue-600">
              <RepeatIcon className="h-4 w-4 mr-1" />
              {task.recurrence_pattern}
            </div>
          )}
        </div>

        {task.tags && task.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {task.tags.map((tag, index) => (
              <Badge key={index} variant="secondary" className="text-xs">
                <TagIcon className="h-3 w-3 mr-1" />
                {tag}
              </Badge>
            ))}
          </div>
        )}
      </CardContent>

      <CardFooter className="flex justify-between pt-2">
        <div className="text-xs text-gray-500">
          Created: {formatDate(task.created_at)}
        </div>
        <Button variant="outline" size="sm" onClick={() => onDelete(task.id)}>
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
};

export default TaskCard;