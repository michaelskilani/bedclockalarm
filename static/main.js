document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "timeGridWeek",
    height: "auto",
    selectable: true,
    slotDuration: "01:00:00",
    select: function (info) {
      var eventData = {
        title: "Alarm",
        start: info.startStr,
        end: info.endStr,
      };
      calendar.addEvent(eventData);

      fetch("/add_off_limit_hours", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          start: info.startStr,
          end: info.endStr,
        }),
      })
        .then((response) => response.json())
        .then((result) => {
          console.log("Alarm time added: ", result["start"], result["end"]);
        })
        .catch((error) => console.error("Error:", error));
    },
    eventClick: function (info) {
      var userConfirmation = confirm("Do you want to delete this event?");
      if (userConfirmation) {
        info.event.remove();
        fetch("/delete_off_limit_hours", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            start: info.event.startStr,
            end: info.event.endStr,
          }),
        })
          .then((response) => response.json())
          .then((result) =>
            console.log("Alarm time deleted: ", result["start"], result["end"])
          )
          .catch((error) => console.error("Error:", error));
      }
    },
  });

  fetch("/get_events")
    .then((response) => response.json())
    .then((events) => {
      events.forEach((event) => {
        event.title = "Alarm";
        calendar.addEvent(event);
      });

      calendar.render();
    })
    .catch((error) => console.error("Error fetching events:", error));
});
