import { fireEvent, render, screen } from '@testing-library/svelte';
import { describe, expect, it, vi } from 'vitest';
import ElderlyPersonForm from '../../../src/components/ElderlyPersonForm.svelte';

describe('ElderlyPersonForm', () => {
    it('should render form fields correctly', () => {
        render(ElderlyPersonForm, {
            props: {
                visible: true,
                title: 'Test Form',
                loading: false
            }
        });

        expect(screen.getByLabelText(/nombre/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/apellido/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/edad/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/dirección/i)).toBeInTheDocument();
    });

    it('should show validation errors for empty required fields', async () => {
        const { component } = render(ElderlyPersonForm, {
            props: {
                visible: true,
                title: 'Test Form',
                loading: false
            }
        });

        const submitButton = screen.getByText(/crear/i);
        await fireEvent.click(submitButton);

        expect(screen.getByText(/nombre y apellido son obligatorios/i)).toBeInTheDocument();
    });

    it('should emit submit event with form data', async () => {
        const mockSubmit = vi.fn();
        const { component } = render(ElderlyPersonForm, {
            props: {
                visible: true,
                title: 'Test Form',
                loading: false
            }
        });

        component.$on('submit', mockSubmit);

        await fireEvent.input(screen.getByLabelText(/nombre/i), { target: { value: 'Juan' } });
        await fireEvent.input(screen.getByLabelText(/apellido/i), { target: { value: 'Pérez' } });
        await fireEvent.input(screen.getByLabelText(/edad/i), { target: { value: '75' } });

        const submitButton = screen.getByText(/crear/i);
        await fireEvent.click(submitButton);

        expect(mockSubmit).toHaveBeenCalledWith(
            expect.objectContaining({
                detail: expect.objectContaining({
                    first_name: 'Juan',
                    last_name: 'Pérez',
                    age: '75'
                })
            })
        );
    });

    it('should show loading state', () => {
        render(ElderlyPersonForm, {
            props: {
                visible: true,
                title: 'Test Form',
                loading: true
            }
        });

        expect(screen.getByText(/guardando/i)).toBeInTheDocument();
        expect(screen.getByText(/guardando/i)).toBeDisabled();
    });
}); 