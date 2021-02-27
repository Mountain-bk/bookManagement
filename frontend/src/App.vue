<template>
  <div id="app">
    <NavBar />
    <div class="container">
      <div class="row">
        <div class="col-8 mx-auto mt-5"></div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";

export default {
  name: "App",
  components: {
    NavBar,
  },
};
</script>

<style>
#app {
  font-family: "Playfair Display", serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}

body {
  background-color: #f1f6f9;
  color: #14274e;
  font-family: "Playfair Display", serif;
  height: 100vh;
  margin: 0;
}

h1 {
  text-align: center;
  font-size: 6rem;
}

a {
  text-decoration: none;
}
</style>
