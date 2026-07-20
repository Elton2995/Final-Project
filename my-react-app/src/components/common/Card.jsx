import React from 'react';
import { motion } from 'framer-motion';

const Card = ({ 
  children, 
  className = '', 
  hover = true,
  padding = 'p-3',
  ...props 
}) => {
  return (
    <motion.div
      whileHover={hover ? { y: -4, boxShadow: '0 8px 24px rgba(0,0,0,0.12)' } : {}}
      className={`card card-custom ${padding} ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default Card;