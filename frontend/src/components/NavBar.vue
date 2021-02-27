<template>
  <div>
    <div class="nav-container">
      <ul class="nav-bar">
        <li>
          <router-link to="/" class="nav-item" href="">Home</router-link>
        </li>
        <li>
          <router-link to="/book-list" class="nav-item" href=""
            >Book List</router-link
          >
        </li>
        <li>
          <router-link to="/book-register" class="nav-item" href=""
            >Add Book</router-link
          >
        </li>
        <li>
          <router-link to="/author-list" class="nav-item" href=""
            >Author</router-link
          >
        </li>
        <li>
          <router-link to="/category-list" class="nav-item" href=""
            >Category</router-link
          >
        </li>
      </ul>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "NavBar",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.nav-bar {
  list-style-type: none;
  margin: 0;
  padding: 10px;
  overflow: hidden;
  background-color: #333;
  display: flex;
}

.nav-item {
  display: inline-block;
  color: white;
  text-align: center;
  padding: 15px 40px;
  text-decoration: none;
}
</style>
