const port_backend: string = import.meta.env.VITE_PORT_BACK;
export const backend_url: string = import.meta.env.VITE_BACKEND_URL || `http://localhost:${port_backend}`;

const port_auth: string = import.meta.env.VITE_PORT_AUTH;
export const auth_url: string = import.meta.env.VITE_AUTH_URL || `http://localhost:${port_auth}`;
