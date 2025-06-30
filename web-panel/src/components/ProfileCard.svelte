<script lang="ts">
    import { createEventDispatcher } from "svelte";
    export let user = {
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        specialization: "",
        is_verified: false,
        role: "Cuidador",
    };
    export let editable = false;
    export let loading = false;
    const dispatch = createEventDispatcher();

    function handleEdit() {
        dispatch("edit");
    }
</script>

<div class="profile-card">
    <h2 class="profile-title">Perfil de Cuidador</h2>
    {#if editable}
        <button class="edit-profile-btn" on:click={handleEdit} title="Editar perfil">Editar perfil</button>
    {/if}
    <div class="profile-info-grid">
        <div>
            <div class="label">Nombre completo</div>
            <div class="info-block">{user.first_name} {user.last_name}</div>
        </div>
        <div>
            <div class="label">Email</div>
            <div class="info-block">{user.email}</div>
        </div>
        <div>
            <div class="label">Teléfono</div>
            <div class="info-block">{user.phone || '-'}</div>
        </div>
        {#if user.specialization}
        <div>
            <div class="label">Especialidad</div>
            <div class="info-block">{user.specialization}</div>
        </div>
        {/if}
        <div>
            <div class="label">Estado</div>
            <div class="info-block">
                <span class="badge {user.is_verified ? 'active' : 'inactive'}">
                    {user.is_verified ? 'Activo' : 'Inactivo'}
                </span>
            </div>
        </div>
    </div>
</div>

<style>
.profile-card {
    position: relative;
    max-width: 420px;
    margin: 0 auto 2rem auto;
    background: #fff;
    border-radius: 1rem;
    box-shadow: 0 2px 12px 0 rgba(37, 99, 235, 0.07);
    padding: 2rem 2rem 1.5rem 2rem;
    border: 1px solid #e5e7eb;
}
@media (max-width: 900px) {
    .profile-card {
        padding: 1.2rem 0.7rem 1rem 0.7rem;
        max-width: 98vw;
    }
}
@media (max-width: 600px) {
    .profile-card {
        padding: 0.7rem 0.3rem 0.7rem 0.3rem;
        max-width: 100vw;
    }
    .profile-title {
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    .profile-info-grid {
        grid-template-columns: 1fr;
        gap: 0.7rem 0;
    }
    .label {
        font-size: 0.95rem;
    }
    .info-block {
        font-size: 1rem;
        padding: 0.4rem 0.5rem;
    }
    .edit-profile-btn {
        font-size: 0.98rem;
        margin-bottom: 0.7rem;
    }
}
.profile-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 1.5rem;
    text-align: left;
}
.profile-info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem 2rem;
}
.label {
    font-size: 0.92rem;
    color: #64748b;
    margin-bottom: 0.2rem;
    font-weight: 500;
}
.info-block {
    font-size: 1.08rem;
    font-weight: 500;
    color: #222;
    background: #f3f6fa;
    border-radius: 0.6rem;
    padding: 0.6rem 0.9rem;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 4px rgba(37,99,235,0.04);
    word-break: break-word;
    min-height: 2.2em;
    display: flex;
    align-items: center;
}
.badge {
    display: inline-block;
    padding: 0.25em 0.8em;
    border-radius: 999px;
    font-size: 0.98em;
    font-weight: 600;
    letter-spacing: 0.01em;
    border: 1px solid #e5e7eb;
}
.badge.active {
    background: #d1fae5;
    color: #047857;
}
.badge.inactive {
    background: #fee2e2;
    color: #b91c1c;
}
.edit-profile-btn {
    display: inline-block;
    margin-bottom: 1.2rem;
    background: #2563eb;
    color: #fff;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    border-radius: 0.5rem;
    padding: 0.45rem 1.2rem;
    cursor: pointer;
    box-shadow: 0 1px 4px rgba(37,99,235,0.07);
    transition: background 0.2s, color 0.2s;
}
.edit-profile-btn:hover {
    background: #1e40af;
    color: #fff;
}
</style>
