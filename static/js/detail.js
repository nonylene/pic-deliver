const ORIGINAL_WIDTH = 1920
const ORIGINAL_HEIGHT = 1080
const FONT_SIZE_PX = 30

onload = () => {
  var pic_path = new URL(window.location).searchParams.get("pic_path")

  var api_url = new URL("/api/detail", window.location)
  api_url.searchParams.append("pic_path", pic_path)

  fetch(api_url).then(response => {
    if (response.ok) {
      return response.json()
    } else {
      throw new Error("network error")
    }
  }).then(load).catch(e => console.log(e))
}

var load = (json) => {
  var background = new Image();
  var canvas = document.getElementById("canvas")
  var table = document.getElementById("characters")
  var ctx = canvas.getContext("2d")
  ctx.font = "bold " + FONT_SIZE_PX + "px sans-serif"
  ctx.strokeStyle = 'red'
  ctx.fillStyle = 'white'
  background.src = json["thumb_url"]

  background.onload = () => {
    var thumb_scale = canvas.height / background.height
    ctx.drawImage(background,
        0, 0, background.width, background.height,
        0, 0, background.width * thumb_scale, background.height * thumb_scale
        )

    json["faces"].forEach((face, index) => {
      ctx.beginPath()
      var original_scale = canvas.height / ORIGINAL_HEIGHT
      ctx.lineWidth = 2
      ctx.strokeRect(
          face.x * original_scale, face.y * original_scale,
          face.w * original_scale, face.h * original_scale
          )

      ctx.lineWidth = 2.5
      var text_x = face.x * original_scale + 5
      var text_y = face.y * original_scale + FONT_SIZE_PX

      ctx.fillText(index, text_x, text_y)
      ctx.strokeText(index, text_x, text_y)

      insert_cells(table.insertRow(-1), face, index)
    })
  }
}

var insert_cells = (row, face, index) => {
  insert_cell(row, index)
  insert_cell(row, face["character"])
  insert_cell(row, face["probability"].toFixed(2))
  insert_cell(row, face["character_1"])
  insert_cell(row, face["probability_1"].toFixed(2))
  insert_cell(row, face["character_2"])
  insert_cell(row, face["probability_2"].toFixed(2))
}

var insert_cell = (row, text) => {
  row.insertCell(-1).appendChild(document.createTextNode(text))
}
