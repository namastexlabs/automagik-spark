// ===================================================================
// ⚡ Automagik-Spark - Standalone PM2 Configuration
// ===================================================================
// This file enables automagik-spark to run independently
// It extracts the same configuration from the central ecosystem

const path = require('path');
const fs = require('fs');

// Get the current directory (automagik-spark)
const PROJECT_ROOT = __dirname;

/**
 * Extract version from pyproject.toml file using standardized approach
 * @param {string} projectPath - Path to the project directory
 * @returns {string} Version string or 'unknown'
 */
function extractVersionFromPyproject(projectPath) {
  const pyprojectPath = path.join(projectPath, 'pyproject.toml');
  
  if (!fs.existsSync(pyprojectPath)) {
    return 'unknown';
  }
  
  try {
    const content = fs.readFileSync(pyprojectPath, 'utf8');
    
    // Standard approach: Static version in [project] section
    const projectVersionMatch = content.match(/\[project\][\s\S]*?version\s*=\s*["']([^"']+)["']/);
    if (projectVersionMatch) {
      return projectVersionMatch[1];
    }
    
    // Fallback: Simple version = "..." pattern anywhere in file
    const simpleVersionMatch = content.match(/^version\s*=\s*["']([^"']+)["']/m);
    if (simpleVersionMatch) {
      return simpleVersionMatch[1];
    }
    
    return 'unknown';
  } catch (error) {
    console.warn(`Failed to read version from ${pyprojectPath}:`, error.message);
    return 'unknown';
  }
}

// Load environment variables from .env file if it exists
const envPath = path.join(PROJECT_ROOT, '.env');
let envVars = {};
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  envContent.split('\n').forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) {
      envVars[key.trim()] = value.trim().replace(/^["']|["']$/g, '');
    }
  });
}

module.exports = {
  apps: [
    // ================================
    // Automagik-Spark API
    // ================================
    {
      name: 'automagik-spark-api',
      cwd: PROJECT_ROOT,
      script: '.venv/bin/uvicorn',
      args: 'automagik_spark.api.app:app --host ' + (envVars.AUTOMAGIK_SPARK_API_HOST || '0.0.0.0') + ' --port ' + (envVars.AUTOMAGIK_SPARK_API_PORT || '8883'),
      interpreter: 'none',
      version: extractVersionFromPyproject(PROJECT_ROOT),
      env: {
        ...envVars,
        PYTHONPATH: PROJECT_ROOT,
        AUTOMAGIK_SPARK_API_HOST: envVars.AUTOMAGIK_SPARK_API_HOST || '0.0.0.0',
        AUTOMAGIK_SPARK_API_PORT: envVars.AUTOMAGIK_SPARK_API_PORT || '8883',
        AUTOMAGIK_SPARK_API_CORS: envVars.AUTOMAGIK_SPARK_API_CORS || 'http://localhost:3000,http://localhost:8883',
        AUTOMAGIK_SPARK_ENV: envVars.AUTOMAGIK_SPARK_ENV || 'production',
        AUTOMAGIK_SPARK_DATABASE_URL: envVars.AUTOMAGIK_SPARK_DATABASE_URL,
        AUTOMAGIK_SPARK_ENCRYPTION_KEY: envVars.AUTOMAGIK_SPARK_ENCRYPTION_KEY,
        AUTOMAGIK_SPARK_REMOTE_URL: envVars.AUTOMAGIK_SPARK_REMOTE_URL,
        AUTOMAGIK_AGENTS_API_HOST: envVars.AUTOMAGIK_AGENTS_API_HOST,
        AUTOMAGIK_AGENTS_API_PORT: envVars.AUTOMAGIK_AGENTS_API_PORT,
        AUTOMAGIK_AGENTS_URL: envVars.AUTOMAGIK_AGENTS_URL,
        LANGFLOW_API_URL: envVars.LANGFLOW_API_URL,
        LANGFLOW_API_KEY: envVars.LANGFLOW_API_KEY || '',
        AUTOMAGIK_TIMEZONE: envVars.AUTOMAGIK_TIMEZONE || 'UTC',
        NODE_ENV: 'production'
      },
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 1000,
      kill_timeout: 5000,
      error_file: path.join(PROJECT_ROOT, 'logs/api-err.log'),
      out_file: path.join(PROJECT_ROOT, 'logs/api-out.log'),
      log_file: path.join(PROJECT_ROOT, 'logs/api-combined.log'),
      merge_logs: true,
      time: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    
    // ================================
    // Automagik-Spark Worker
    // ================================
    {
      name: 'automagik-spark-worker',
      cwd: PROJECT_ROOT,
      script: '.venv/bin/celery',
      args: '-A automagik_spark.core.celery.celery_app worker --loglevel=' + (envVars.AUTOMAGIK_SPARK_LOG_LEVEL || 'info').toLowerCase(),
      interpreter: 'none',
      version: extractVersionFromPyproject(PROJECT_ROOT),
      env: {
        ...envVars,
        PYTHONPATH: PROJECT_ROOT,
        AUTOMAGIK_SPARK_ENV: envVars.AUTOMAGIK_SPARK_ENV || 'production',
        AUTOMAGIK_SPARK_DATABASE_URL: envVars.AUTOMAGIK_SPARK_DATABASE_URL,
        AUTOMAGIK_SPARK_CELERY_BROKER_URL: envVars.AUTOMAGIK_SPARK_CELERY_BROKER_URL,
        AUTOMAGIK_SPARK_CELERY_RESULT_BACKEND: envVars.AUTOMAGIK_SPARK_CELERY_RESULT_BACKEND,
        AUTOMAGIK_SPARK_ENCRYPTION_KEY: envVars.AUTOMAGIK_SPARK_ENCRYPTION_KEY,
        AUTOMAGIK_SPARK_WORKER_LOG: envVars.AUTOMAGIK_SPARK_WORKER_LOG,
        AUTOMAGIK_TIMEZONE: envVars.AUTOMAGIK_TIMEZONE || 'UTC',
        LANGFLOW_API_URL: envVars.LANGFLOW_API_URL,
        LANGFLOW_API_KEY: envVars.LANGFLOW_API_KEY || '',
        NODE_ENV: 'production'
      },
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 1000,
      kill_timeout: 5000,
      error_file: path.join(PROJECT_ROOT, 'logs/worker-err.log'),
      out_file: path.join(PROJECT_ROOT, 'logs/worker-out.log'),
      log_file: path.join(PROJECT_ROOT, 'logs/worker-combined.log'),
      merge_logs: true,
      time: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    }
  ]
};