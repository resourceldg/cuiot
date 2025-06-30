<script lang="ts">
  import { goto } from '$app/navigation';
  export let user = {
    first_name: '',
    last_name: '',
    roles: [], // array de strings
    avatar_url: '', // opcional
  };
  export let onLogout = () => {};

  let open = false;
  let dropdownRef;

  function clickOutside(node) {
    const handleClick = (event) => {
      if (node && !node.contains(event.target)) {
        open = false;
      }
    };
    document.addEventListener('mousedown', handleClick, true);
    return {
      destroy() {
        document.removeEventListener('mousedown', handleClick, true);
      }
    };
  }

  function getInitials() {
    if (user.first_name && user.last_name) {
      return user.first_name[0].toUpperCase() + user.last_name[0].toUpperCase();
    }
    if (user.first_name) return user.first_name[0].toUpperCase();
    return '?';
  }
  function getDisplayName() {
    if (user.first_name) {
      return user.first_name;
    }
    return 'Sin nombre';
  }
  function getRole() {
    if (user.roles && user.roles.length > 0) return user.roles[0];
    return 'Usuario';
  }
  function goToProfile() {
    goto('/dashboard/profile');
    open = false;
  }
  function handleLogout() {
    onLogout();
    open = false;
  }
</script>

<div class="profile-menu" bind:this={dropdownRef} use:clickOutside>
  <button class="profile-trigger" aria-haspopup="true" aria-expanded={open} on:click={() => (open = !open)}>
    {#if user.avatar_url}
      <img src={user.avatar_url} alt="Avatar" class="avatar" />
    {:else}
      <div class="avatar initials">{getInitials()}</div>
    {/if}
    <div class="profile-info">
      <span class="profile-name">{getDisplayName()}</span>
      <span class="profile-role">{getRole()}</span>
    </div>
    <svg class="chevron" width="20" height="20" viewBox="0 0 20 20"><path d="M6 8l4 4 4-4" stroke="#555" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
  </button>
  {#if open}
    <div class="dropdown-menu">
      <button class="dropdown-item" on:click={goToProfile}>Ver perfil</button>
      <button class="dropdown-item" on:click={handleLogout}>Cerrar sesión</button>
    </div>
  {/if}
</div>

<style>
.profile-menu {
  position: relative;
  display: flex;
  align-items: center;
}
.profile-trigger {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px 14px 6px 6px;
  border-radius: 24px;
  transition: background 0.18s;
  min-width: 0;
  box-shadow: none;
}
.profile-trigger:focus {
  outline: 2px solid #2563eb;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #2563eb;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  margin-right: 12px;
  object-fit: cover;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  border: 2px solid #fff;
}
.avatar.initials {
  background: linear-gradient(135deg, #2563eb 60%, #60a5fa 100%);
}
.profile-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-right: 8px;
}
.profile-name {
  font-size: 1rem;
  font-weight: 600;
  color: #222;
  line-height: 1.1;
}
.profile-role {
  font-size: 0.85rem;
  color: #2563eb;
  font-weight: 500;
  margin-top: 2px;
}
.chevron {
  margin-left: 4px;
  transition: transform 0.2s;
  pointer-events: none;
}
.profile-trigger[aria-expanded="true"] .chevron {
  transform: rotate(180deg);
}
.dropdown-menu {
  position: absolute;
  top: 110%;
  right: 0;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 24px 0 rgba(37, 99, 235, 0.12);
  min-width: 170px;
  z-index: 100;
  padding: 8px 0;
  display: flex;
  flex-direction: column;
  animation: fadeIn 0.18s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}
.dropdown-item {
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  padding: 10px 20px;
  font-size: 1rem;
  color: #222;
  cursor: pointer;
  transition: background 0.15s;
}
.dropdown-item:hover {
  background: #f3f4f6;
  color: #2563eb;
}
@media (max-width: 600px) {
  .profile-info { display: none; }
  .profile-trigger { padding: 6px; }
  .avatar { margin-right: 0; }
}
</style> 