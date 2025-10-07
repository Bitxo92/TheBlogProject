<script>
  import { Mail, Lock, Loader2, Eye, EyeOff, User } from "lucide-svelte";
  import { onMount } from "svelte";

  let email = $state("");
  let password = $state("");
  let username = $state("");
  let first_name = $state("");
  let last_name = $state("");
  let confirmPassword = $state("");
  let msg_error = $state("");
  let loading = $state(false);
  let showPassword = $state(false);

  async function handleRegister() {
    loading = true;
    msg_error = "";
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          email,
          first_name,
          last_name,
          password,
        }),
      });
      const data = await response.json();
      if (!response.ok) msg_error = data.detail || "Login failed";
    } catch (error) {
      msg_error = "Network error. Please try again.";
    } finally {
      loading = false;
    }
  }

  function togglePassword() {
    showPassword = !showPassword;
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
    <legend class="fieldset-legend">Register</legend>

    <label class="label" for="username">
      Username <User class="inline w-4 h-4 ml-1" />
    </label>
    <input
      id="username"
      type="text"
      class="input validator"
      required
      placeholder="Username"
      pattern="[A-Za-z][A-Za-z0-9\-]*"
      minlength="3"
      maxlength="30"
      title="Only letters, numbers or dash"
    />
    <p class="validator-hint">
      Must be 3 to 30 characters
      <br />containing only letters, numbers or dash
    </p>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 items-start">
      <div>
        <label class="label mb-1" for="first_name">
          First name <User class="inline w-4 h-4 ml-1 mb-1" />
        </label>
        <input
          id="first_name"
          name="first_name"
          type="text"
          class="input validator"
          required
          placeholder="First name"
        />
      </div>
      <div>
        <label class="label mb-1" for="last_name">
          Last name <User class="inline w-4 h-4 ml-1 mb-1" />
        </label>
        <input
          id="last_name"
          name="last_name"
          type="text"
          class="input validator"
          required
          placeholder="Last name"
        />
      </div>
    </div>

    <label class="label" for="email">
      Email <Mail class="inline w-4 h-4 ml-1" />
    </label>
    <input
      id="email"
      type="email"
      class="input validator"
      required
      placeholder="mail@site.com"
      title="Enter your email address"
      bind:value={email}
      disabled={loading}
    />
    <div class="validator-hint">Enter valid email address</div>

    <label class="label" for="password">
      Password <Lock class="inline w-4 h-4 ml-1" />
    </label>
    <div class="relative">
      <input
        id="password"
        type={showPassword ? "text" : "password"}
        class="input validator"
        required
        placeholder="Password"
        minlength="8"
        pattern="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).&#123;8,&#125;$"
        title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
        bind:value={password}
        disabled={loading}
      />

      <button
        type="button"
        class="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover: cursor-pointer"
        onclick={togglePassword}
        tabindex="-1"
      >
        {#if showPassword}
          <EyeOff class="w-5 h-5" />
        {:else}
          <Eye class="w-5 h-5" />
        {/if}
      </button>
    </div>

    <label class="label" for="confirmPassword">
      ConfirmPassword <Lock class="inline w-4 h-4 ml-1" />
    </label>
    <div class="relative">
      <input
        id="confirmPassword"
        type={showPassword ? "text" : "password"}
        class="input validator"
        required
        placeholder="Confirm Password"
        minlength="8"
        pattern="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).&#123;8,&#125;$"
        title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
        bind:value={confirmPassword}
        disabled={loading}
      />

      <button
        type="button"
        class="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover: cursor-pointer"
        onclick={togglePassword}
        tabindex="-1"
      >
        {#if showPassword}
          <EyeOff class="w-5 h-5" />
        {:else}
          <Eye class="w-5 h-5" />
        {/if}
      </button>
    </div>

    <p class="validator-hint">
      Must be more than 8 characters, including
      <br />At least one number
      <br />At least one lowercase letter
      <br />At least one uppercase letter
    </p>

    <button
      class="btn btn-neutral mt-4 w-full"
      onclick={handleRegister}
      disabled={loading}
    >
      {#if loading}
        <Loader2 class="w-4 h-4 animate-spin mr-2" />
        Creating Account...
      {:else}
        Register
      {/if}
    </button>

    <div class="mt-5 text-center">
      <p>
        Already have an account? <a href="/login" class="link link-primary"
          >Login</a
        >
      </p>
      {#if msg_error}
        <p class="text-sm mt-2 text-error">{msg_error}</p>
      {/if}
    </div>
  </fieldset>
</div>
