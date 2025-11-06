'use client';

import { useState } from 'react';

interface Section {
  database_id: number;
  name: string;
  status: string;
}

interface ProgressSidebarProps {
  currentSection: Section | null;
  selectedAgent: string;
}

// Define all sections for founder-buddy
const FOUNDER_BUDDY_SECTIONS = [
  { id: 'mission', name: 'Mission', displayName: 'Mission' },
  { id: 'idea', name: 'Idea', displayName: 'Idea' },
  { id: 'team_traction', name: 'Team & Traction', displayName: 'Team & Traction' },
  { id: 'invest_plan', name: 'Investment Plan', displayName: 'Investment Plan' }
];

export default function ProgressSidebar({ currentSection, selectedAgent }: ProgressSidebarProps) {
  const [isOpen, setIsOpen] = useState(false);

  const getSectionTitle = (agentId: string) => {
    if (agentId === 'value-canvas') return 'Current Section';
    if (agentId === 'social-pitch') return 'Current Component';
    if (agentId === 'mission-pitch') return 'Current Stage';
    if (agentId === 'special-report') return 'Current Section';
    return 'Progress';
  };

  // Get status for a section
  const getSectionStatus = (sectionId: string): 'pending' | 'in_progress' | 'completed' => {
    if (!currentSection) return 'pending';
    
    // Match by section name (case-insensitive)
    const currentSectionName = currentSection.name.toLowerCase();
    const sectionName = sectionId.toLowerCase();
    
    // Check if this is the current section
    if (currentSectionName.includes(sectionName) || sectionName.includes(currentSectionName)) {
      if (currentSection.status === 'completed' || currentSection.status === 'done') {
        return 'completed';
      }
      return 'in_progress';
    }
    
    // Check if sections before this one are completed
    const currentIndex = FOUNDER_BUDDY_SECTIONS.findIndex(s => 
      currentSectionName.includes(s.id) || currentSectionName.includes(s.name.toLowerCase())
    );
    const sectionIndex = FOUNDER_BUDDY_SECTIONS.findIndex(s => s.id === sectionId);
    
    if (currentIndex > sectionIndex) {
      return 'completed';
    }
    
    return 'pending';
  };

  // Get display name for current section
  const getCurrentSectionDisplayName = () => {
    if (!currentSection) return 'Select a section';
    
    // Try to match with our defined sections
    const matched = FOUNDER_BUDDY_SECTIONS.find(s => 
      currentSection.name.toLowerCase().includes(s.id) || 
      currentSection.name.toLowerCase().includes(s.name.toLowerCase())
    );
    
    return matched ? matched.displayName : currentSection.name;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
      case 'done':
        return '#10b981'; // green
      case 'in_progress':
        return '#6366f1'; // purple
      default:
        return '#94a3b8'; // gray
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
      case 'done':
        return 'Done';
      case 'in_progress':
        return 'In Progress';
      default:
        return 'Pending';
    }
  };

  // Only show dropdown for founder-buddy
  if (selectedAgent !== 'founder-buddy') {
    return (
      <div style={{
        display: 'flex',
        gap: '12px',
        alignItems: 'center'
      }}>
        <div style={{
          fontSize: '12px',
          fontWeight: '600',
          color: '#64748b',
          whiteSpace: 'nowrap'
        }}>
          {getSectionTitle(selectedAgent)}:
        </div>
        
        {currentSection ? (
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <div style={{
              padding: '6px 12px',
              backgroundColor: '#f8fafc',
              borderRadius: '6px',
              border: '1px solid #e2e8f0',
              fontSize: '12px',
              color: '#1e293b',
              fontWeight: '500'
            }}>
              #{currentSection.database_id}
            </div>

            <div style={{
              padding: '6px 12px',
              backgroundColor: '#f8fafc',
              borderRadius: '6px',
              border: '1px solid #e2e8f0',
              fontSize: '12px',
              color: '#1e293b',
              fontWeight: '500'
            }}>
              {currentSection.name}
            </div>

            <div style={{
              padding: '6px 12px',
              backgroundColor: '#f8fafc',
              borderRadius: '6px',
              border: '1px solid #e2e8f0',
              fontSize: '12px',
              fontWeight: '500',
              color: currentSection.status === 'pending' ? '#f59e0b' :
                     currentSection.status === 'completed' ? '#10b981' : '#6366f1',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              <span style={{
                width: '6px',
                height: '6px',
                borderRadius: '50%',
                backgroundColor: currentSection.status === 'pending' ? '#f59e0b' :
                               currentSection.status === 'completed' ? '#10b981' : '#6366f1'
              }}></span>
              {currentSection.status.charAt(0).toUpperCase() + currentSection.status.slice(1)}
            </div>
          </div>
        ) : (
          <div style={{
            fontSize: '12px',
            color: '#94a3b8',
            fontStyle: 'italic'
          }}>
            {selectedAgent ? 'Start a conversation to see progress' : 'Select an agent to begin'}
          </div>
        )}
      </div>
    );
  }

  return (
    <div style={{
      display: 'flex',
      gap: '12px',
      alignItems: 'center',
      position: 'relative'
    }}>
      <div style={{
        fontSize: '12px',
        fontWeight: '600',
        color: '#64748b',
        whiteSpace: 'nowrap'
      }}>
        {getSectionTitle(selectedAgent)}:
      </div>
      
      <div style={{ position: 'relative', minWidth: '200px' }}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          style={{
            width: '100%',
            padding: '8px 12px',
            backgroundColor: '#f8fafc',
            border: '1px solid #e2e8f0',
            borderRadius: '6px',
            fontSize: '12px',
            color: '#1e293b',
            fontWeight: '500',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '8px',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = '#f1f5f9';
            e.currentTarget.style.borderColor = '#cbd5e1';
          }}
          onMouseLeave={(e) => {
            if (!isOpen) {
              e.currentTarget.style.backgroundColor = '#f8fafc';
              e.currentTarget.style.borderColor = '#e2e8f0';
            }
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1 }}>
            {currentSection ? (
              <>
                <span style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  backgroundColor: getStatusColor(currentSection.status)
                }}></span>
                <span>{getCurrentSectionDisplayName()}</span>
                <span style={{
                  fontSize: '10px',
                  color: '#94a3b8',
                  marginLeft: 'auto'
                }}>
                  {getStatusText(currentSection.status)}
                </span>
              </>
            ) : (
              <span style={{ color: '#94a3b8' }}>Select a section</span>
            )}
          </div>
          <span style={{
            fontSize: '10px',
            color: '#64748b',
            transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s ease'
          }}>▼</span>
        </button>

        {isOpen && (
          <>
            <div
              onClick={() => setIsOpen(false)}
              style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                zIndex: 998
              }}
            />
            <div style={{
              position: 'absolute',
              top: '100%',
              left: 0,
              right: 0,
              marginTop: '4px',
              backgroundColor: 'white',
              border: '1px solid #e2e8f0',
              borderRadius: '6px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
              zIndex: 999,
              overflow: 'hidden',
              maxHeight: '300px',
              overflowY: 'auto'
            }}>
              {FOUNDER_BUDDY_SECTIONS.map((section) => {
                const status = getSectionStatus(section.id);
                const isCurrent = currentSection && (
                  currentSection.name.toLowerCase().includes(section.id) ||
                  currentSection.name.toLowerCase().includes(section.name.toLowerCase())
                );

                return (
                  <div
                    key={section.id}
                    onClick={() => {
                      setIsOpen(false);
                      // Could add navigation logic here if needed
                    }}
                    style={{
                      padding: '10px 12px',
                      cursor: 'pointer',
                      backgroundColor: isCurrent ? '#f0f9ff' : 'white',
                      borderLeft: isCurrent ? '3px solid #6366f1' : '3px solid transparent',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '8px',
                      transition: 'background-color 0.15s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = '#f8fafc';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = isCurrent ? '#f0f9ff' : 'white';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1 }}>
                      <span style={{
                        width: '6px',
                        height: '6px',
                        borderRadius: '50%',
                        backgroundColor: getStatusColor(status)
                      }}></span>
                      <span style={{
                        fontSize: '12px',
                        fontWeight: isCurrent ? '600' : '500',
                        color: '#1e293b'
                      }}>
                        {section.displayName}
                      </span>
                    </div>
                    <span style={{
                      fontSize: '10px',
                      color: getStatusColor(status),
                      fontWeight: '500'
                    }}>
                      {getStatusText(status)}
                    </span>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
}