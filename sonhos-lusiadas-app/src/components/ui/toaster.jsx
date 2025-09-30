import { Toaster as SonnerToaster } from "sonner"

export function Toaster() {
  return (
    <SonnerToaster
      position="top-right"
      toastOptions={{
        style: {
          background: 'white',
          color: '#111827',
          border: '1px solid #e2e8f0',
        },
      }}
    />
  )
}
