import React, { useState, useEffect } from 'react'
import { Excalidraw } from '@excalidraw/excalidraw'

interface ExcalidrawWrapperProps {
  initialData: {
    elements: any[]
    appState?: Record<string, any>
  } | null
  viewModeEnabled?: boolean
  zenModeEnabled?: boolean
}

export default function ExcalidrawWrapper({
  initialData,
  viewModeEnabled = true,
  zenModeEnabled = false,
}: ExcalidrawWrapperProps) {
  const [excalidrawAPI, setExcalidrawAPI] = useState<any>(null)

  useEffect(() => {
    if (excalidrawAPI && initialData) {
      excalidrawAPI.updateScene({
        elements: initialData.elements,
        appState: initialData.appState || {},
      })
    }
  }, [initialData, excalidrawAPI])

  return (
    <div style={{ height: '100%', width: '100%' }}>
      <Excalidraw
        initialData={initialData || undefined}
        viewModeEnabled={viewModeEnabled}
        zenModeEnabled={zenModeEnabled}
        UIOptions={{
          canvasActions: {
            changeViewBackgroundColor: false,
            export: { saveFileToDisk: true },
          },
        }}
        excalidrawAPI={(api: any) => setExcalidrawAPI(api)}
      />
    </div>
  )
}
