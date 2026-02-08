'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRightIcon, CheckCircleIcon, CalendarIcon, FlagIcon, RepeatIcon } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="max-w-4xl mx-auto text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Advanced Task Management
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Streamline your productivity with our AI-powered task management system featuring
            recurring tasks, due dates, priorities, tags, and smart filtering.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link href="/dashboard">
              <Button size="lg" className="px-8 py-3 text-lg">
                Go to Dashboard
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/tasks">
              <Button size="lg" variant="outline" className="px-8 py-3 text-lg">
                Manage Tasks
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          <Card>
            <CardHeader>
              <div className="flex items-center mb-2">
                <CheckCircleIcon className="h-6 w-6 text-green-500 mr-2" />
                <CardTitle>Smart Tracking</CardTitle>
              </div>
              <CardDescription>Automatically track and manage your tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Keep everything organized with our intuitive task management system that remembers what you need to do.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center mb-2">
                <CalendarIcon className="h-6 w-6 text-blue-500 mr-2" />
                <CardTitle>Due Dates</CardTitle>
              </div>
              <CardDescription>Never miss a deadline with due date tracking</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Set due dates for your tasks and receive timely reminders to stay on schedule.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center mb-2">
                <FlagIcon className="h-6 w-6 text-red-500 mr-2" />
                <CardTitle>Priorities</CardTitle>
              </div>
              <CardDescription>Focus on what matters most</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Assign priority levels to tasks so you always know what to tackle first.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center mb-2">
                <RepeatIcon className="h-6 w-6 text-purple-500 mr-2" />
                <CardTitle>Recurring Tasks</CardTitle>
              </div>
              <CardDescription>Automate repetitive tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Create tasks that repeat daily, weekly, monthly, or yearly to save time.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center mb-2">
                <FlagIcon className="h-6 w-6 text-indigo-500 mr-2" />
                <CardTitle>Tagging System</CardTitle>
              </div>
              <CardDescription>Categorize and filter your tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Organize tasks with custom tags for easy searching and filtering.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center mb-2">
                <CheckCircleIcon className="h-6 w-6 text-teal-500 mr-2" />
                <CardTitle>Progress Tracking</CardTitle>
              </div>
              <CardDescription>Visualize your productivity</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Track your progress with insightful statistics and completion rates.</p>
            </CardContent>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="max-w-2xl mx-auto text-center">
          <Card>
            <CardHeader>
              <CardTitle>Ready to boost your productivity?</CardTitle>
              <CardDescription>
                Join thousands of users who trust our platform to manage their tasks efficiently.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/dashboard">
                <Button size="lg" className="w-full md:w-auto">
                  Get Started Now
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default HomePage;