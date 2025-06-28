import { fireEvent, render, screen } from '@testing-library/svelte';
import { describe, expect, it, vi } from 'vitest';
import EventForm from '../../../src/components/EventForm.svelte';

describe('EventForm', () => {
    it('should render form fields correctly', () => {
        render(EventForm, {
            props: {
                visible: true,
                title: 'Test Event Form',
                loading: false
            }
        });

        expect(screen.getByLabelText(/título/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/tipo de evento/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/inicio/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/fin/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/ubicación/i)).toBeInTheDocument();
    });

    it('should show validation errors for empty required fields', async () => {
        const { component } = render(EventForm, {
            props: {
                visible: true,
                title: 'Test Event Form',
                loading: false
            }
        });

        const submitButton = screen.getByText(/crear evento/i);
        await fireEvent.click(submitButton);

        expect(screen.getByText(/el título es obligatorio/i)).toBeInTheDocument();
    });

    it('should validate date range correctly', async () => {
        const { component } = render(EventForm, {
            props: {
                visible: true,
                title: 'Test Event Form',
                loading: false
            }
        });

        // Fill required fields
        await fireEvent.input(screen.getByLabelText(/título/i), { target: { value: 'Test Event' } });

        // Set invalid date range (end before start)
        const startInput = screen.getByLabelText(/inicio/i);
        const endInput = screen.getByLabelText(/fin/i);

        await fireEvent.input(startInput, { target: { value: '2024-07-01T10:00' } });
        await fireEvent.input(endInput, { target: { value: '2024-07-01T09:00' } });

        const submitButton = screen.getByText(/crear evento/i);
        await fireEvent.click(submitButton);

        expect(screen.getByText(/la fecha\/hora de fin no puede ser anterior al inicio/i)).toBeInTheDocument();
    });

    it('should emit submit event with form data', async () => {
        const mockSubmit = vi.fn();
        const { component } = render(EventForm, {
            props: {
                visible: true,
                title: 'Test Event Form',
                loading: false
            }
        });

        component.$on('submit', mockSubmit);

        await fireEvent.input(screen.getByLabelText(/título/i), { target: { value: 'Test Event' } });
        await fireEvent.input(screen.getByLabelText(/inicio/i), { target: { value: '2024-07-01T10:00' } });
        await fireEvent.input(screen.getByLabelText(/fin/i), { target: { value: '2024-07-01T11:00' } });

        const submitButton = screen.getByText(/crear evento/i);
        await fireEvent.click(submitButton);

        expect(mockSubmit).toHaveBeenCalledWith(
            expect.objectContaining({
                detail: expect.objectContaining({
                    title: 'Test Event',
                    start_datetime: expect.any(String),
                    end_datetime: expect.any(String)
                })
            })
        );
    });
}); 