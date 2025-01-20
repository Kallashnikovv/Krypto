import React, { useState } from "react"; 
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell } from "@fortawesome/free-solid-svg-icons";
import "./NotificationBell.css";

const NotificationBell = () => {
  console.log("Komponent NotificationBell działa!");

  const [showNotifications, setShowNotifications] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [notifications, setNotifications] = useState([
    "Powiadomienie 1: Bardzo długa wiadomość dotycząca czegoś ważnego",
    "Powiadomienie 2: Krótsza wiadomość",
    "Powiadomienie 3: Średniej długości tekst",
    "Powiadomienie 4: Wiadomość testowa",
    "Powiadomienie 5: Kolejne powiadomienie",
    "Powiadomienie 6: Ważna informacja",
    "Powiadomienie 7: Ostatnie powiadomienie na liście"
  ]);

  const removeNotification = (index) => {
    const updatedNotifications = notifications.filter((_, i) => i !== index);
    setNotifications(updatedNotifications);
  };

  const renderNotificationMessage = () => {
    const visibleNotifications = showAll ? notifications : notifications.slice(0, 5);

    return visibleNotifications.map((notification, index) => (
      <div key={index} className="notification-item">
        <p>{notification}</p>
        <button
          className="remove-btn"
          onClick={() => removeNotification(index)}
        >
          X
        </button>
      </div>
    ));
  };

  return (
    <div
      className="notification-bell"
      onMouseEnter={() => setShowNotifications(true)}
      onMouseLeave={() => setShowNotifications(false)}
    >
      <FontAwesomeIcon icon={faBell} className="bell-icon" />
      {notifications.length > 0 && (
        <span className="notification-badge">
          {notifications.length > 99 ? "99+" : notifications.length}
        </span>
      )}
      {showNotifications && (
        <div className="notifications-panel">
          {notifications.length > 0 ? (
            <p className="notifications-header"> NOTIFICATIONS: </p>
          ) : (
            <p className="notifications-header"> NO NOTIFICATIONS </p>
          )}
          {renderNotificationMessage()}
          {notifications.length > 5 && !showAll && (
            <button
              className="show-all-btn"
              onClick={() => setShowAll(true)}
            >
              SHOW ALL NOTIFICATIONS
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationBell;
