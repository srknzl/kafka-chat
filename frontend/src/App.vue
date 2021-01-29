<template>

  <div id="app">
    <div>
      <p>Real Time Kafka Chat</p>
      <p>Usage</p>
      <ul>
        <li>Everyone's message appears in the same list below</li>
        <li>You can press enter(when input is focused) to send messages or press send button</li>
        <li>Reload to try connecting again if the websocket is not ready</li>
      </ul>
      <p>Technologies</p>
      <ul>
        <li>Kafka is used for message streaming and storage.</li>
        <li>Websocket is used for showing and sending messages without a reload need.</li>
        <li>Asyncio is used for asynchronous usage of Kafka.</li>
      </ul>
    </div>
    <label for="username-input">Your name</label>
    <input id="username-input" v-model="username">

    <div id="messages">
      <div id="message-box" v-for="message in messages" :key="message.timestamp">
        <div style="width: 80%">
          <p>{{ message.message }}</p>
        </div>
        <div style="width: 20%">
          <p>{{ (new Date(message.timestamp)).toLocaleString("en-us") }}</p>
        </div>
      </div>
      <div id="input-box">
        <div style="width: 80%">
          <input id="message-input" v-on:keyup.enter="sendMessage()" v-model="userInput" placeholder="Your message">
        </div>
        <div style="width: 20%">
          <button id="submit-button" v-on:click="sendMessage()">Send</button>
        </div>
      </div>
    </div>

    <p>Server Status: {{ status }}</p>
  </div>


</template>

<script>


export default {
  name: 'App',
  components: {},
  mounted() {
    this.ws = new WebSocket('ws://localhost:3000');
    this.ws.addEventListener('open', () => {
      this.status = "Connection established"
      this.canSendMessage = true;
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
      this.status = "Connection lost"
      console.log("Error connecting to server ", event);
    })

  },
  data: function () {
    return {
      messages: [],
      userInput: "",
      ws: null,
      canSendMessage: false,
      status: "",
      username: "Anonymous"
    }

  },
  computed: {},
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
        alert("Websocket not ready, if you just run the application, wait up to 30 second for kafka and websocket server to be ready. Reload to try again");
      } else {
        this.ws.send(JSON.stringify({
          message: this.username + " : " + this.userInput,
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
  color: #2c3e50;
  margin-top: 60px;
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

p {
  overflow-wrap: anywhere
}

#messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid rgba(0, 0, 0, .5);
  border-radius: 0.3rem;
  width: 90%;
  background: rgba(255, 255, 162, 0.2);
}

#message-box {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  border: 1px solid rgba(0, 0, 0, .2);
  border-radius: 0.3rem;
  margin: 0.5rem;
  padding: 0.5rem;
  width: 80%;
  flex-wrap: wrap;
  background: rgba(60, 58, 58, 0.2);
}

#message-input {
  width: 100%;
  padding: 0;
  border: none;
  height: 2.5rem;
  background: rgba(233, 226, 226, 0.2);
  font-size: large;
}

#username-input {
  width: 20%;
  padding: 0;
  height: 2.5rem;
  background: rgba(233, 226, 226, 0.2);
  font-size: large;
}


#input-box {
  border: 1px solid rgba(0, 103, 28, .4);
  width: 80%;
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 0.5rem;
  padding: 0.5rem;
}

#input:focus {
  outline: none;
}

#submit-button {
  width: 100%;
  height: 2.5rem;
}
</style>
