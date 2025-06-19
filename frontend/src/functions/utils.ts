const port_backend: string = import.meta.env.VITE_PORT_BACK;
export const backend_url: string = import.meta.env.VITE_BACKEND_URL || `http://localhost:${port_backend}`;
