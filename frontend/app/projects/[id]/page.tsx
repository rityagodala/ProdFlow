'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { apiClient } from '@/lib/api'
import Link from 'next/link'

interface Task {
  id: number
  title: string
  description: string | null
  status: 'todo' | 'in_progress' | 'done'
  assignee_id: number | null
}

interface Project {
  id: number
  name: string
  description: string | null
}

export default function ProjectDetailPage() {
  const { isAuthenticated, loading: authLoading } = useAuth()
  const router = useRouter()
  const params = useParams()
  const projectId = parseInt(params.id as string)

  const [project, setProject] = useState<Project | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [taskTitle, setTaskTitle] = useState('')
  const [taskDescription, setTaskDescription] = useState('')
  const [taskStatus, setTaskStatus] = useState<'todo' | 'in_progress' | 'done'>('todo')

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, authLoading, router])

  useEffect(() => {
    if (isAuthenticated && projectId) {
      loadProject()
      loadTasks()
    }
  }, [isAuthenticated, projectId])

  const loadProject = async () => {
    try {
      const data = await apiClient.getProject(projectId)
      setProject(data)
    } catch (err: any) {
      setError('Failed to load project')
    }
  }

  const loadTasks = async () => {
    try {
      const data = await apiClient.getTasks(projectId)
      setTasks(data)
    } catch (err: any) {
      setError('Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiClient.createTask(projectId, taskTitle, taskDescription, taskStatus)
      setTaskTitle('')
      setTaskDescription('')
      setTaskStatus('todo')
      setShowCreateForm(false)
      await loadTasks()
    } catch (err: any) {
      setError('Failed to create task')
    }
  }

  const handleUpdateTaskStatus = async (taskId: number, newStatus: 'todo' | 'in_progress' | 'done') => {
    try {
      await apiClient.updateTask(projectId, taskId, undefined, undefined, newStatus)
      await loadTasks()
    } catch (err: any) {
      setError('Failed to update task')
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return
    try {
      await apiClient.deleteTask(projectId, taskId)
      await loadTasks()
    } catch (err: any) {
      setError('Failed to delete task')
    }
  }

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  const statusColors = {
    todo: 'bg-gray-200 text-gray-800',
    in_progress: 'bg-yellow-200 text-yellow-800',
    done: 'bg-green-200 text-green-800',
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/dashboard" className="text-gray-700 hover:text-gray-900 mr-4">
                ← Back to Dashboard
              </Link>
              <h1 className="text-xl font-semibold text-gray-900">
                {project?.name || 'Project'}
              </h1>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {project && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{project.name}</h2>
              {project.description && (
                <p className="text-gray-600">{project.description}</p>
              )}
            </div>
          )}

          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-800">{error}</div>
            </div>
          )}

          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold text-gray-900">Tasks</h3>
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              {showCreateForm ? 'Cancel' : 'New Task'}
            </button>
          </div>

          {showCreateForm && (
            <form onSubmit={handleCreateTask} className="mb-6 bg-white p-4 rounded-lg shadow">
              <div className="mb-4">
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                  Task Title
                </label>
                <input
                  id="title"
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500"
                  value={taskTitle}
                  onChange={(e) => setTaskTitle(e.target.value)}
                />
              </div>
              <div className="mb-4">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  id="description"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500"
                  value={taskDescription}
                  onChange={(e) => setTaskDescription(e.target.value)}
                />
              </div>
              <div className="mb-4">
                <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  id="status"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500"
                  value={taskStatus}
                  onChange={(e) => setTaskStatus(e.target.value as 'todo' | 'in_progress' | 'done')}
                >
                  <option value="todo">Todo</option>
                  <option value="in_progress">In Progress</option>
                  <option value="done">Done</option>
                </select>
              </div>
              <button
                type="submit"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Create Task
              </button>
            </form>
          )}

          {tasks.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No tasks yet. Create your first task!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {tasks.map((task) => (
                <div key={task.id} className="bg-white rounded-lg shadow p-6">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="text-lg font-semibold text-gray-900">{task.title}</h4>
                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="text-red-600 hover:text-red-800 text-sm font-medium"
                    >
                      Delete
                    </button>
                  </div>
                  {task.description && (
                    <p className="text-sm text-gray-600 mb-4">{task.description}</p>
                  )}
                  <div className="flex items-center gap-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[task.status]}`}>
                      {task.status.replace('_', ' ').toUpperCase()}
                    </span>
                    <select
                      value={task.status}
                      onChange={(e) => handleUpdateTaskStatus(task.id, e.target.value as 'todo' | 'in_progress' | 'done')}
                      className="text-sm border border-gray-300 rounded-md px-2 py-1"
                    >
                      <option value="todo">Todo</option>
                      <option value="in_progress">In Progress</option>
                      <option value="done">Done</option>
                    </select>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

