import React from 'react';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ size = 'md', text = 'Loading...' }) => {
  const sizeMap = {
    sm: { width: 32, height: 32 },
    md: { width: 48, height: 48 },
    lg: { width: 64, height: 64 }
  };

  const dimensions = sizeMap[size] || sizeMap.md;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="d-flex flex-column align-items-center justify-content-center p-5"
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        style={{ width: dimensions.width, height: dimensions.height }}
        className="border-4 border-primary border-top-transparent rounded-circle"
      />
      {text && <p className="mt-3 text-muted">{text}</p>}
    </motion.div>
  );
};

export default LoadingSpinner;