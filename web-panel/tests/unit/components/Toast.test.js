import { fireEvent, render, screen } from '@testing-library/svelte';
import { describe, expect, it, vi } from 'vitest';
import Toast from '../../../src/components/Toast.svelte';

describe('Toast', () => {
    it('should render success message correctly', () => {
        render(Toast, {
            props: {
                visible: true,
                message: 'Operación exitosa',
                type: 'success'
            }
        });

        expect(screen.getByText('Operación exitosa')).toBeInTheDocument();
        expect(screen.getByRole('alert')).toHaveClass('toast-success');
    });

    it('should render error message correctly', () => {
        render(Toast, {
            props: {
                visible: true,
                message: 'Error en la operación',
                type: 'error'
            }
        });

        expect(screen.getByText('Error en la operación')).toBeInTheDocument();
        expect(screen.getByRole('alert')).toHaveClass('toast-error');
    });

    it('should emit close event when close button is clicked', async () => {
        const mockClose = vi.fn();
        const { component } = render(Toast, {
            props: {
                visible: true,
                message: 'Test message',
                type: 'success'
            }
        });

        component.$on('close', mockClose);

        const closeButton = screen.getByRole('button', { name: /cerrar/i });
        await fireEvent.click(closeButton);

        expect(mockClose).toHaveBeenCalled();
    });

    it('should auto-hide after specified duration', async () => {
        const mockClose = vi.fn();
        const { component } = render(Toast, {
            props: {
                visible: true,
                message: 'Test message',
                type: 'success',
                duration: 1000
            }
        });

        component.$on('close', mockClose);

        // Wait for auto-hide
        await new Promise(resolve => setTimeout(resolve, 1100));

        expect(mockClose).toHaveBeenCalled();
    });
}); 