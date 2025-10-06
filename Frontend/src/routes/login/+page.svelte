<script>
  import { Mail, Lock, Loader2 } from "lucide-svelte";
  import { onMount } from "svelte";

  let email = "";
  let password = "";
  let msg_error = "";
  let loading = false;

  async function handleLogin() {
    loading = true;
    msg_error = "";
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);
      const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) msg_error = data.detail || "Login failed";
    } catch (error) {
      msg_error = "Network error. Please try again.";
    } finally {
      loading = false;
    }
  }
</script>

<div class="relative flex justify-center items-center min-h-screen bg-base-100">
  {#if loading}
    <div
      class="absolute inset-0 bg-base-200/50 backdrop-blur-sm flex flex-col justify-center items-center z-10"
    >
      <Loader2 class="w-10 h-10 animate-spin text-white" />
      <p class="mt-2 text-white">Signing in...</p>
    </div>
  {/if}

  <fieldset
    class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4 transition-all duration-300"
    class:blur-sm={loading}
  >
    <legend class="fieldset-legend">Login</legend>

    <label class="label" for="email">
      Email <Mail class="inline w-4 h-4 ml-1" />
    </label>
    <input
      id="email"
      type="email"
      class="input"
      placeholder="Email"
      bind:value={email}
      disabled={loading}
    />

    <label class="label" for="password">
      Password <Lock class="inline w-4 h-4 ml-1" />
    </label>
    <input
      id="password"
      type="password"
      class="input"
      placeholder="Password"
      bind:value={password}
      disabled={loading}
    />

    <button
      class="btn btn-neutral mt-4 w-full"
      on:click={handleLogin}
      disabled={loading}
    >
      {#if loading}
        <Loader2 class="w-4 h-4 animate-spin mr-2" />
        Logging in...
      {:else}
        Login
      {/if}
    </button>

    <div class="mt-5 text-center">
      <p>
        Don’t have an account? <a href="/register" class="link link-primary"
          >Register</a
        >
      </p>
      {#if msg_error}
        <p class="text-sm mt-2 text-error">{msg_error}</p>
      {:else}
        <p class="text-sm mt-2 text-success">Login Succesfull!</p>
      {/if}
    </div>
  </fieldset>
</div>
