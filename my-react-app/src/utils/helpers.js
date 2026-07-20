/**
 * Format a date string to a readable format
 */
export const formatDate = (dateString, format = 'default') => {
  const date = new Date(dateString);
  const options = {
    default: { month: 'short', day: 'numeric', year: 'numeric' },
    full: { month: 'long', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' },
    time: { hour: '2-digit', minute: '2-digit' },
    short: { month: 'short', day: 'numeric' }
  };
  
  return date.toLocaleDateString('en-US', options[format] || options.default);
};

/**
 * Truncate text to a specified length
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
};

/**
 * Generate a random ID
 */
export const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};

/**
 * Debounce function for search inputs
 */
export const debounce = (func, delay = 300) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

/**
 * Check if a string is a valid email
 */
export const isValidEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

/**
 * Get status color for badges
 */
export const getStatusColor = (status) => {
  const colors = {
    open: 'warning',
    inprogress: 'primary',
    resolved: 'success',
    closed: 'secondary',
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  };
  return colors[status] || 'secondary';
};

/**
 * Get priority color
 */
export const getPriorityColor = (priority) => {
  const colors = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  };
  return colors[priority] || 'secondary';
};

/**
 * Format file size
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

/**
 * Get initials from a name
 */
export const getInitials = (name) => {
  if (!name) return '?';
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};