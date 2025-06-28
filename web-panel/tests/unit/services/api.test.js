import { beforeEach, describe, expect, it, vi } from 'vitest';
import { authService, elderlyPersonService, eventService } from '../../../src/lib/api.js';

// Mock fetch globally
global.fetch = vi.fn();

describe('API Services', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        localStorage.clear();
    });

    describe('authService', () => {
        it('should login successfully', async () => {
            const mockResponse = {
                access_token: 'test-token',
                token_type: 'bearer'
            };

            fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => mockResponse
            });

            const result = await authService.login('test@example.com', 'password');

            expect(result).toEqual(mockResponse);
            expect(localStorage.getItem('token')).toBe('test-token');
        });

        it('should handle login errors', async () => {
            fetch.mockResolvedValueOnce({
                ok: false,
                status: 401,
                json: async () => ({ detail: 'Invalid credentials' })
            });

            await expect(authService.login('test@example.com', 'wrong-password'))
                .rejects.toThrow('Invalid credentials');
        });

        it('should logout correctly', () => {
            localStorage.setItem('token', 'test-token');

            authService.logout();

            expect(localStorage.getItem('token')).toBeNull();
        });
    });

    describe('elderlyPersonService', () => {
        it('should get all elderly persons', async () => {
            const mockResponse = [
                { id: '1', first_name: 'Juan', last_name: 'Pérez' }
            ];

            fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => mockResponse
            });

            const result = await elderlyPersonService.getAll();

            expect(result).toEqual(mockResponse);
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/v1/elderly-persons/'),
                expect.objectContaining({
                    headers: expect.objectContaining({
                        'Authorization': 'Bearer test-token'
                    })
                })
            );
        });

        it('should create elderly person', async () => {
            const mockData = {
                first_name: 'Juan',
                last_name: 'Pérez',
                age: 75
            };

            const mockResponse = { id: '1', ...mockData };

            fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => mockResponse
            });

            const result = await elderlyPersonService.create(mockData);

            expect(result).toEqual(mockResponse);
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining('/api/v1/elderly-persons/'),
                expect.objectContaining({
                    method: 'POST',
                    body: JSON.stringify(mockData)
                })
            );
        });
    });

    describe('eventService', () => {
        it('should get all events', async () => {
            const mockResponse = [
                { id: '1', title: 'Test Event', event_type: 'medical' }
            ];

            fetch.mockResolvedValueOnce({
                ok: true,
                json: async () => mockResponse
            });

            const result = await eventService.getAll();

            expect(result).toEqual(mockResponse);
        });
    });
}); 