import React, { useState } from 'react';
import type { AnalyzeResponse } from '../types/satquery';
import { FileText, Code, Check } from 'lucide-react';

interface ReportDownloadProps {
  response: AnalyzeResponse;
  query?: string;
}

export const ReportDownload: React.FC<ReportDownloadProps> = ({
  response,
}) => {
  const [downloadingFormat, setDownloadingFormat] = useState<'pdf' | 'json' | null>(null);

  const handleDownloadJSON = () => {
    setDownloadingFormat('json');
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(response, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `SatQuery_Report_${response.sessionId}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();

    setTimeout(() => setDownloadingFormat(null), 1500);
  };

  const handleDownloadPDF = () => {
    setDownloadingFormat('pdf');
    // For prototype demonstration, generate print view or styled download
    window.print();
    setTimeout(() => setDownloadingFormat(null), 1500);
  };

  return (
    <div style={{
      background: 'rgba(12, 19, 36, 0.8)',
      border: '1px solid var(--border-subtle)',
      borderRadius: 'var(--radius-md)',
      padding: '16px 20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: 12
    }}>
      <div>
        <h4 style={{ fontSize: 13, fontWeight: 700, margin: '0 0 2px', color: '#ffffff' }}>
          Downloadable Evidence Report (SPDD §9.6 Parity)
        </h4>
        <p style={{ fontSize: 11, color: 'var(--text-muted)', margin: 0 }}>
          Exports grounded response, visual evidence coordinates, confidence tier, and full audit trace table.
        </p>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <button
          onClick={handleDownloadPDF}
          className="btn-secondary"
          style={{ fontSize: 12, padding: '8px 14px' }}
        >
          {downloadingFormat === 'pdf' ? <Check size={14} color="var(--emerald-success)" /> : <FileText size={14} color="var(--cyan-primary)" />}
          <span>Download PDF Report</span>
        </button>

        <button
          onClick={handleDownloadJSON}
          className="btn-secondary"
          style={{ fontSize: 12, padding: '8px 14px' }}
        >
          {downloadingFormat === 'json' ? <Check size={14} color="var(--emerald-success)" /> : <Code size={14} color="var(--indigo-primary)" />}
          <span>Export Trace (JSON)</span>
        </button>
      </div>
    </div>
  );
};
