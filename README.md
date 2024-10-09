# alma-api
<a href="https://stats.uptimerobot.com/0HCIzTy1EG/">
  <img src="https://img.shields.io/uptimerobot/status/m797562430-1dd4c1addad4402b1e688c4d" alt="UptimeRobot Badge">
</a>

- please refer to the [documentation](https://alma-api.onrender.com/docs) for the different possible endpoints and header parameters.
- data is fetched with python using aiohttp, asynchronously, and then parsed using selectolax and HTMLParser. lastly, it is fed back to the user through the API using FastAPI.
- some endpoints were created to support the almate app: home-info, overall-info, and ai-info are some of them
