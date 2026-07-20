import React from 'react';
import { FolderOpen } from 'lucide-react';

const EmptyState = ({ 
  title = 'Nothing to show', 
  description = 'No items found', 
  actionText, 
  onAction,
  icon: Icon = FolderOpen 
}) => {
  return (
    <div className="text-center py-5">
      <div className="bg-light p-4 rounded-circle d-inline-block mb-4">
        <Icon size={48} className="text-muted" />
      </div>
      <h5 className="fw-bold">{title}</h5>
      <p className="text-muted">{description}</p>
      {actionText && onAction && (
        <button className="btn btn-primary mt-3" onClick={onAction}>
          {actionText}
        </button>
      )}
    </div>
  );
};

export default EmptyState;