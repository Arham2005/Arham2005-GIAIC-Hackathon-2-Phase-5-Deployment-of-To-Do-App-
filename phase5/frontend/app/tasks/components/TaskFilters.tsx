'use client';

import React, { useState } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { CalendarIcon, SearchIcon, FilterIcon } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';
import { Checkbox } from '@/components/ui/checkbox';

interface TaskFilterProps {
  onFilterChange: (filters: any) => void;
}

const TaskFilters = ({ onFilterChange }: TaskFilterProps) => {
  const [completed, setCompleted] = useState<string | null>(null);
  const [priority, setPriority] = useState<string>('');
  const [tags, setTags] = useState<string[]>([]);
  const [dueDateFrom, setDueDateFrom] = useState<Date | undefined>(undefined);
  const [dueDateTo, setDueDateTo] = useState<Date | undefined>(undefined);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<string>('asc');

  const priorities = ['low', 'medium', 'high', 'urgent'];
  const availableTags = ['work', 'personal', 'urgent', 'meeting', 'follow-up'];

  const applyFilters = () => {
    const filters = {
      completed: completed === 'all' ? null : completed === 'true',
      priority: priority || undefined,
      tags: tags.length > 0 ? tags : undefined,
      due_date_from: dueDateFrom ? dueDateFrom.toISOString() : undefined,
      due_date_to: dueDateTo ? dueDateTo.toISOString() : undefined,
      search_query: searchQuery || undefined,
      sort_by: sortBy,
      sort_order: sortOrder
    };

    onFilterChange(filters);
  };

  const resetFilters = () => {
    setCompleted(null);
    setPriority('');
    setTags([]);
    setDueDateFrom(undefined);
    setDueDateTo(undefined);
    setSearchQuery('');
    setSortBy('created_at');
    setSortOrder('asc');

    onFilterChange({
      completed: null,
      priority: undefined,
      tags: undefined,
      due_date_from: undefined,
      due_date_to: undefined,
      search_query: undefined,
      sort_by: 'created_at',
      sort_order: 'asc'
    });
  };

  return (
    <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
      <div className="flex items-center gap-2 mb-4">
        <FilterIcon className="h-5 w-5 text-gray-600" />
        <h3 className="font-medium">Filters</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div>
          <label className="block text-sm font-medium mb-1">Search</label>
          <div className="relative">
            <SearchIcon className="absolute left-2 top-2.5 h-4 w-4 text-gray-500" />
            <Input
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8"
            />
          </div>
        </div>

        {/* Completion Status */}
        <div>
          <label className="block text-sm font-medium mb-1">Status</label>
          <Select value={completed || ''} onValueChange={(value) => setCompleted(value || null)}>
            <SelectTrigger>
              <SelectValue placeholder="All" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All</SelectItem>
              <SelectItem value="false">Pending</SelectItem>
              <SelectItem value="true">Completed</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Priority */}
        <div>
          <label className="block text-sm font-medium mb-1">Priority</label>
          <Select value={priority} onValueChange={setPriority}>
            <SelectTrigger>
              <SelectValue placeholder="All Priorities" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All Priorities</SelectItem>
              {priorities.map((p) => (
                <SelectItem key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Sort Options */}
        <div>
          <label className="block text-sm font-medium mb-1">Sort By</label>
          <div className="flex gap-2">
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-[50%]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="created_at">Created Date</SelectItem>
                <SelectItem value="due_date">Due Date</SelectItem>
                <SelectItem value="priority">Priority</SelectItem>
              </SelectContent>
            </Select>
            <Select value={sortOrder} onValueChange={setSortOrder}>
              <SelectTrigger className="w-[50%]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="asc">Ascending</SelectItem>
                <SelectItem value="desc">Descending</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* Date Range and Tags */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Due Date From */}
        <div>
          <label className="block text-sm font-medium mb-1">Due From</label>
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className={`w-full justify-start text-left font-normal ${!dueDateFrom && "text-muted-foreground"}`}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {dueDateFrom ? dueDateFrom.toLocaleDateString() : <span>Pick a date</span>}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={dueDateFrom}
                onSelect={setDueDateFrom}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>

        {/* Due Date To */}
        <div>
          <label className="block text-sm font-medium mb-1">Due To</label>
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className={`w-full justify-start text-left font-normal ${!dueDateTo && "text-muted-foreground"}`}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {dueDateTo ? dueDateTo.toLocaleDateString() : <span>Pick a date</span>}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={dueDateTo}
                onSelect={setDueDateTo}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>

        {/* Tags */}
        <div>
          <label className="block text-sm font-medium mb-1">Tags</label>
          <div className="flex flex-wrap gap-2">
            {availableTags.map((tag) => (
              <div key={tag} className="flex items-center space-x-2">
                <Checkbox
                  id={tag}
                  checked={tags.includes(tag)}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      setTags([...tags, tag]);
                    } else {
                      setTags(tags.filter(t => t !== tag));
                    }
                  }}
                />
                <label htmlFor={tag} className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  {tag}
                </label>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-end gap-2 pt-2">
        <Button variant="outline" onClick={resetFilters}>
          Reset
        </Button>
        <Button onClick={applyFilters}>
          Apply Filters
        </Button>
      </div>
    </div>
  );
};

export default TaskFilters;