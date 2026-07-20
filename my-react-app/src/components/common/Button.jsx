import React from 'react';
import { motion } from 'framer-motion';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  icon: Icon, 
  iconPosition = 'left',
  loading = false,
  disabled = false,
  ...props 
}) => {
  const sizeClasses = {
    sm: 'btn-sm',
    md: '',
    lg: 'btn-lg'
  };

  const baseClass = `btn btn-${variant} ${sizeClasses[size]} ${className}`;

  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={baseClass}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className="spinner-border spinner-border-sm me-2" role="status" />
      )}
      {Icon && iconPosition === 'left' && !loading && <Icon size={18} className="me-2" />}
      {children}
      {Icon && iconPosition === 'right' && <Icon size={18} className="ms-2" />}
    </motion.button>
  );
};

export default Button;