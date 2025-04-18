-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 19. Apr, 2025 00:55 AM
-- Tjener-versjon: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `food_delivery`
--

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `delivery`
--

CREATE TABLE `delivery` (
  `deliveryID` int(11) NOT NULL,
  `orderID` int(11) DEFAULT NULL,
  `driverID` int(11) DEFAULT NULL,
  `deliveryStatus` varchar(100) DEFAULT NULL,
  `deliveryNote` text DEFAULT NULL,
  `phoneNrUser` varchar(20) DEFAULT NULL,
  `deliveryTime` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `delivery`
--

INSERT INTO `delivery` (`deliveryID`, `orderID`, `driverID`, `deliveryStatus`, `deliveryNote`, `phoneNrUser`, `deliveryTime`) VALUES
(1, 1, 1, 'Levert', 'Sett utenfor døren', '22222222', '2025-04-19 00:48:29'),
(2, 2, 2, 'Avbrutt', 'Ring ved ankomst', '33333333', '2025-04-19 00:48:29');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `driver`
--

CREATE TABLE `driver` (
  `driverID` int(11) NOT NULL,
  `fName` varchar(50) DEFAULT NULL,
  `lName` varchar(50) DEFAULT NULL,
  `phoneNr` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `available` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `driver`
--

INSERT INTO `driver` (`driverID`, `fName`, `lName`, `phoneNr`, `email`, `available`) VALUES
(1, 'Jonas', 'Bakke', '90012345', 'jonas@levering.no', 1),
(2, 'Marie', 'Hansen', '90123456', 'marie@levering.no', 1);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `fooditem`
--

CREATE TABLE `fooditem` (
  `itemID` int(11) NOT NULL,
  `restaurantID` int(11) NOT NULL,
  `productID` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `fooditem`
--

INSERT INTO `fooditem` (`itemID`, `restaurantID`, `productID`, `price`, `available`) VALUES
(1, 1, 1, 129.00, 1),
(2, 1, 4, 29.00, 1),
(3, 2, 2, 139.00, 1),
(4, 2, 3, 39.00, 1),
(5, 2, 4, 29.00, 1);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `itemordered`
--

CREATE TABLE `itemordered` (
  `itemOrderID` int(11) NOT NULL,
  `orderID` int(11) DEFAULT NULL,
  `itemID` int(11) DEFAULT NULL,
  `menuID` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `itemordered`
--

INSERT INTO `itemordered` (`itemOrderID`, `orderID`, `itemID`, `menuID`, `quantity`) VALUES
(1, 1, 1, NULL, 1),
(2, 1, 4, NULL, 1),
(3, 2, 2, NULL, 1),
(4, 2, 3, NULL, 1),
(5, 2, 4, NULL, 1);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `menu`
--

CREATE TABLE `menu` (
  `menuID` int(11) NOT NULL,
  `menuName` varchar(100) DEFAULT NULL,
  `restaurantID` int(11) NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `menu`
--

INSERT INTO `menu` (`menuID`, `menuName`, `restaurantID`, `price`, `description`) VALUES
(1, 'Pizza Deal', 1, 149.00, 'Margherita Pizza + Cola'),
(2, 'Burger Meal', 2, 169.00, 'Classic Burger + Fries + Cola');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `menuitem`
--

CREATE TABLE `menuitem` (
  `menuID` int(11) NOT NULL,
  `productID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `menuitem`
--

INSERT INTO `menuitem` (`menuID`, `productID`) VALUES
(1, 1),
(1, 4),
(2, 2),
(2, 3),
(2, 4);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `ordered`
--

CREATE TABLE `ordered` (
  `orderID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `menuID` int(11) NOT NULL,
  `orderTime` datetime DEFAULT current_timestamp(),
  `status` varchar(50) DEFAULT 'Mottatt'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `ordered`
--

INSERT INTO `ordered` (`orderID`, `userID`, `menuID`, `orderTime`, `status`) VALUES
(1, 1, 1, '2025-04-19 00:02:58', 'Underveis'),
(2, 1, 2, '2025-04-19 00:03:22', 'Mottatt'),
(3, 2, 1, '2025-04-19 00:39:34', 'Mottatt'),
(4, 2, 1, '2025-04-19 00:39:34', 'Mottatt'),
(5, 2, 1, '2025-04-19 00:39:35', 'Mottatt'),
(6, 2, 2, '2025-04-19 00:40:16', 'Mottatt'),
(7, 2, 2, '2025-04-19 00:40:17', 'Mottatt'),
(8, 2, 2, '2025-04-19 00:40:17', 'Mottatt');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `product`
--

CREATE TABLE `product` (
  `productID` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `product`
--

INSERT INTO `product` (`productID`, `name`, `description`) VALUES
(1, 'Margherita Pizza', 'Tomatsaus, ost og basilikum'),
(2, 'Burger Classic', 'Briochebrød, biff, ost og salat'),
(3, 'Pommes Frites', 'Sprø potetbiter'),
(4, 'Cola', '0,5L Kullsyreholdig leskedrikk'),
(5, 'Fanta', '');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `restaurant`
--

CREATE TABLE `restaurant` (
  `restaurantID` int(11) NOT NULL,
  `rName` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phoneNr` varchar(20) DEFAULT NULL,
  `openingTime` time DEFAULT NULL,
  `closingTime` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `restaurant`
--

INSERT INTO `restaurant` (`restaurantID`, `rName`, `address`, `phoneNr`, `openingTime`, `closingTime`) VALUES
(1, 'PizzaHuset', 'Pizzaveien 1', '12345678', '10:00:00', '22:00:00'),
(2, 'BurgerKing', 'Burgergata 2', '87654321', '11:00:00', '23:00:00');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `restaurant_admins`
--

CREATE TABLE `restaurant_admins` (
  `user_id` int(11) NOT NULL,
  `restaurantID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `restaurant_admins`
--

INSERT INTO `restaurant_admins` (`user_id`, `restaurantID`) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 1),
(3, 2);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `users`
--

CREATE TABLE `users` (
  `userID` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `fName` varchar(50) DEFAULT NULL,
  `lName` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phoneNr` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `users`
--

INSERT INTO `users` (`userID`, `username`, `fName`, `lName`, `address`, `phoneNr`, `email`, `password`) VALUES
(1, 'admin', 'Admin', 'Adminsen', 'Adminveien 1', '11111111', 'admin@example.com', 'pass123'),
(2, 'pizzabruker', 'Lise', 'Pizza', 'Pizzaveien 2', '22222222', 'lise@pizza.no', 'p123'),
(3, 'burgerbruker', 'Jonas', 'Burger', 'Burgergata 3', '33333333', 'jonas@burger.no', 'burger123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `delivery`
--
ALTER TABLE `delivery`
  ADD PRIMARY KEY (`deliveryID`),
  ADD KEY `orderID` (`orderID`),
  ADD KEY `driverID` (`driverID`);

--
-- Indexes for table `driver`
--
ALTER TABLE `driver`
  ADD PRIMARY KEY (`driverID`);

--
-- Indexes for table `fooditem`
--
ALTER TABLE `fooditem`
  ADD PRIMARY KEY (`itemID`),
  ADD KEY `restaurantID` (`restaurantID`),
  ADD KEY `productID` (`productID`);

--
-- Indexes for table `itemordered`
--
ALTER TABLE `itemordered`
  ADD PRIMARY KEY (`itemOrderID`),
  ADD KEY `orderID` (`orderID`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menuID`),
  ADD KEY `restaurantID` (`restaurantID`);

--
-- Indexes for table `menuitem`
--
ALTER TABLE `menuitem`
  ADD PRIMARY KEY (`menuID`,`productID`),
  ADD KEY `productID` (`productID`);

--
-- Indexes for table `ordered`
--
ALTER TABLE `ordered`
  ADD PRIMARY KEY (`orderID`),
  ADD KEY `userID` (`userID`),
  ADD KEY `menuID` (`menuID`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`productID`);

--
-- Indexes for table `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`restaurantID`);

--
-- Indexes for table `restaurant_admins`
--
ALTER TABLE `restaurant_admins`
  ADD PRIMARY KEY (`user_id`,`restaurantID`),
  ADD KEY `restaurantID` (`restaurantID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `delivery`
--
ALTER TABLE `delivery`
  MODIFY `deliveryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `driver`
--
ALTER TABLE `driver`
  MODIFY `driverID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `fooditem`
--
ALTER TABLE `fooditem`
  MODIFY `itemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `itemordered`
--
ALTER TABLE `itemordered`
  MODIFY `itemOrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `menuID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ordered`
--
ALTER TABLE `ordered`
  MODIFY `orderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `productID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `restaurantID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Begrensninger for dumpede tabeller
--

--
-- Begrensninger for tabell `delivery`
--
ALTER TABLE `delivery`
  ADD CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `ordered` (`orderID`) ON DELETE CASCADE,
  ADD CONSTRAINT `delivery_ibfk_2` FOREIGN KEY (`driverID`) REFERENCES `driver` (`driverID`) ON DELETE SET NULL;

--
-- Begrensninger for tabell `fooditem`
--
ALTER TABLE `fooditem`
  ADD CONSTRAINT `fooditem_ibfk_1` FOREIGN KEY (`restaurantID`) REFERENCES `restaurant` (`restaurantID`) ON DELETE CASCADE,
  ADD CONSTRAINT `fooditem_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `product` (`productID`) ON DELETE CASCADE;

--
-- Begrensninger for tabell `itemordered`
--
ALTER TABLE `itemordered`
  ADD CONSTRAINT `itemordered_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `ordered` (`orderID`) ON DELETE CASCADE;

--
-- Begrensninger for tabell `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`restaurantID`) REFERENCES `restaurant` (`restaurantID`) ON DELETE CASCADE;

--
-- Begrensninger for tabell `menuitem`
--
ALTER TABLE `menuitem`
  ADD CONSTRAINT `menuitem_ibfk_1` FOREIGN KEY (`menuID`) REFERENCES `menu` (`menuID`) ON DELETE CASCADE,
  ADD CONSTRAINT `menuitem_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `product` (`productID`) ON DELETE CASCADE;

--
-- Begrensninger for tabell `ordered`
--
ALTER TABLE `ordered`
  ADD CONSTRAINT `ordered_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE,
  ADD CONSTRAINT `ordered_ibfk_2` FOREIGN KEY (`menuID`) REFERENCES `menu` (`menuID`) ON DELETE CASCADE;

--
-- Begrensninger for tabell `restaurant_admins`
--
ALTER TABLE `restaurant_admins`
  ADD CONSTRAINT `restaurant_admins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`userID`) ON DELETE CASCADE,
  ADD CONSTRAINT `restaurant_admins_ibfk_2` FOREIGN KEY (`restaurantID`) REFERENCES `restaurant` (`restaurantID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
