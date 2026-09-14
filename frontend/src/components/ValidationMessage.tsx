import React from 'react';
import { AlertTriangle, Info, CheckCircle } from 'lucide-react';

interface ValidationMessageProps {
  type?: 'warning' | 'info' | 'success';
  message: string;
  details?: string;
}

export const ValidationMessage: React.FC<ValidationMessageProps> = ({
  type = 'info',
  message,
  details
}) => {
  const styles = {
    warning: {
      color: 'var(--amber-warning)',
      bg: 'rgba(245, 158, 11, 0.08)',
      border: 'rgba(245, 158, 11, 0.3)',
      icon: <AlertTriangle size={16} color="var(--amber-warning)" />
    },
    info: {
      color: 'var(--cyan-primary)',
      bg: 'rgba(56, 189, 248, 0.08)',
      border: 'rgba(56, 189, 248, 0.3)',
      icon: <Info size={16} color="var(--cyan-primary)" />
    },
    success: {
      color: 'var(--emerald-success)',
      bg: 'rgba(16, 185, 129, 0.08)',
      border: 'rgba(16, 185, 129, 0.3)',
      icon: <CheckCircle size={16} color="var(--emerald-success)" />
    }
  }[type];

  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-start',
      gap: 10,
      padding: '10px 14px',
      borderRadius: 'var(--radius-sm)',
      background: styles.bg,
      border: `1px solid ${styles.border}`,
      marginBottom: 16
    }}>
      <div style={{ marginTop: 2 }}>{styles.icon}</div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 12, fontWeight: 600, color: '#ffffff' }}>
          {message}
        </div>
        {details && (
          <div style={{ fontSize: 11, color: 'var(--text-secondary)', marginTop: 2 }}>
            {details}
          </div>
        )}
      </div>
    </div>
  );
};
