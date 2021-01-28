<template>

  <div id="app">
    <p v-for="message in messages" :key="message.timestamp">{{ message.message }} at
      {{ (new Date(message.timestamp)).toLocaleString("en-us") }}</p>
    <div>
      <p>Server Status: {{ status }}</p>
      <input v-model="userInput" placeholder="Your message">
      <button v-on:click="sendMessage()">Click</button>
      <p>{{ infoMessage }}</p>
      <p>{{ errorMessage }}</p>
    </div>
  </div>


</template>

<script>


export default {
  name: 'App',
  components: {},
  mounted() {
    this.ws = new WebSocket('ws://localhost:3000');
    this.ws.addEventListener('open', () => {
      this.canSendMessage = true;
      this.infoMessage = "";
    });
    // Listen for messages
    this.ws.addEventListener('message', (event) => {
      try {
        const data = JSON.parse(event.data);
        this.addMessage(data);
      } catch (err) {
        console.log(err)
      }

    });
    this.ws.addEventListener('error', (event) => {
      console.log("Error connecting to server ", event);
      this.errorMessage = JSON.stringify(event)
    })

  },
  data: function () {
    return {
      messages: [],
      userInput: "",
      ws: null,
      canSendMessage: false,
      infoMessage: "",
      errorMessage: ""
    }

  },
  computed: {
    status() {
      if (!this.ws) return "";
      if (this.ws.readyState === WebSocket.CLOSED) {
        return "CLOSED"
      } else if (this.ws.readyState === WebSocket.OPEN) {
        return "OPEN"
      } else if (this.ws.readyState === WebSocket.CONNECTING) {
        return "CONNECTING"
      } else if (this.ws.readyState === WebSocket.CLOSING) {
        return "CLOSING"
      } else {
        return ""
      }
    }
  },
  methods: {
    addMessage(data) {
      console.log("New message ", data)
      this.messages.push({
        message: data.message,
        timestamp: data.timestamp
      })
    },
    sendMessage() {
      if (!this.canSendMessage) {
        this.infoMessage = "Please wait for connection to server";
      } else {
        this.infoMessage = "";
        this.ws.send(JSON.stringify({
          message: this.userInput,
          timestamp: new Date().getTime()
        }));
      }

    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
