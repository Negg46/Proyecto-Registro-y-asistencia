-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 10-03-2026 a las 22:25:46
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `registro_casino`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

DROP TABLE IF EXISTS `asistencias`;
DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `Id_Cliente` int NOT NULL AUTO_INCREMENT,
  `Nombre_Completo` varchar(150) NOT NULL,
  `Numero_Identificacion` varchar(20) NOT NULL,
  `Telefono` varchar(20) DEFAULT NULL,
  `Correo_Electronico` varchar(100) DEFAULT NULL,
  `Fecha_Nacimiento` date DEFAULT NULL,
  `Nivel_Cliente` enum('Clasica','VIP') NOT NULL,
  `Numero_Tarjeta` varchar(20) NOT NULL,
  `Fecha_Registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Fecha_VIP` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`Id_Cliente`),
  UNIQUE KEY `Numero_Identificacion` (`Numero_Identificacion`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Estructura de tabla para la tabla `asistencias`
--
CREATE TABLE IF NOT EXISTS `asistencias` (
  `Id_Asistencia` int NOT NULL AUTO_INCREMENT,
  `Id_Cliente` int NOT NULL,
  `Fecha_Asistencia` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id_Asistencia`),
  KEY `Id_Cliente` (`Id_Cliente`),
  CONSTRAINT `fk_asistencias_clientes` FOREIGN KEY (`Id_Cliente`) REFERENCES `clientes` (`Id_Cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`Id_Cliente`, `Nombre_Completo`, `Numero_Identificacion`, `Telefono`, `Correo_Electronico`, `Fecha_Nacimiento`, `Nivel_Cliente`, `Numero_Tarjeta`, `Fecha_Registro`) VALUES
(1, 'Juan Miguel Carreño', '1097493234', '3242253587', 'juanmiguel@correo.com', '2006-04-22', 'Clasica', '54165423156', '2026-03-10 22:16:58'),
(2, 'María González', '1234567890', '3001234567', 'maria@example.com', '1990-05-15', 'Clasica', '123456789012', '2026-03-11 10:00:00'),
(3, 'Carlos Rodríguez', '0987654321', '3019876543', 'carlos@example.com', '1985-08-20', 'Clasica', '987654321098', '2026-03-11 11:30:00'),
(4, 'Ana López', '1122334455', '3021122334', 'ana@example.com', '1995-12-10', 'Clasica', '112233445566', '2026-03-11 12:00:00'),
(5, 'Pedro Sánchez', '5566778899', '3035566778', 'pedro@example.com', '1980-03-25', 'Clasica', '556677889900', '2026-03-11 13:15:00'),
(6, 'Laura Martínez', '6677889900', '3046677889', 'laura@example.com', '1992-07-30', 'Clasica', '667788990011', '2026-03-11 14:45:00'),
(7, 'Diego Fernández', '7788990011', '3057788990', 'diego@example.com', '1988-11-05', 'Clasica', '778899001122', '2026-03-11 15:20:00'),
(8, 'Sofia Ramírez', '8899001122', '3068899001', 'sofia@example.com', '1998-01-18', 'Clasica', '889900112233', '2026-03-11 16:00:00'),
(9, 'Javier Torres', '9900112233', '3079900112', 'javier@example.com', '1975-09-12', 'Clasica', '990011223344', '2026-03-11 17:30:00'),
(10, 'Elena Morales', '0011223344', '3080011223', 'elena@example.com', '1993-04-08', 'Clasica', '001122334455', '2026-03-11 18:00:00');

--
-- Volcado de datos para la tabla `asistencias`
--

INSERT INTO `asistencias` (`Id_Asistencia`, `Id_Cliente`, `Fecha_Asistencia`) VALUES
-- Cliente 2: 16 asistencias en marzo 2026 → Debería ser VIP
(1, 2, '2026-03-01 09:00:00'),
(2, 2, '2026-03-02 10:00:00'),
(3, 2, '2026-03-03 11:00:00'),
(4, 2, '2026-03-04 12:00:00'),
(5, 2, '2026-03-05 13:00:00'),
(6, 2, '2026-03-06 14:00:00'),
(7, 2, '2026-03-07 15:00:00'),
(8, 2, '2026-03-08 16:00:00'),
(9, 2, '2026-03-09 17:00:00'),
(10, 2, '2026-03-10 18:00:00'),
(11, 2, '2026-03-11 19:00:00'),
(12, 2, '2026-03-12 20:00:00'),
(13, 2, '2026-03-13 21:00:00'),
(14, 2, '2026-03-14 22:00:00'),
(15, 2, '2026-03-15 23:00:00'),
(16, 2, '2026-03-16 08:00:00'),

-- Cliente 3: 10 asistencias en marzo → Clásica
(17, 3, '2026-03-01 09:30:00'),
(18, 3, '2026-03-02 10:30:00'),
(19, 3, '2026-03-03 11:30:00'),
(20, 3, '2026-03-04 12:30:00'),
(21, 3, '2026-03-05 13:30:00'),
(22, 3, '2026-03-06 14:30:00'),
(23, 3, '2026-03-07 15:30:00'),
(24, 3, '2026-03-08 16:30:00'),
(25, 3, '2026-03-09 17:30:00'),
(26, 3, '2026-03-10 18:30:00'),

-- Cliente 4: 15 asistencias en marzo → VIP
(27, 4, '2026-03-01 10:00:00'),
(28, 4, '2026-03-02 11:00:00'),
(29, 4, '2026-03-03 12:00:00'),
(30, 4, '2026-03-04 13:00:00'),
(31, 4, '2026-03-05 14:00:00'),
(32, 4, '2026-03-06 15:00:00'),
(33, 4, '2026-03-07 16:00:00'),
(34, 4, '2026-03-08 17:00:00'),
(35, 4, '2026-03-09 18:00:00'),
(36, 4, '2026-03-10 19:00:00'),
(37, 4, '2026-03-11 20:00:00'),
(38, 4, '2026-03-12 21:00:00'),
(39, 4, '2026-03-13 22:00:00'),
(40, 4, '2026-03-14 23:00:00'),
(41, 4, '2026-03-15 00:00:00'),

-- Cliente 5: 5 asistencias → Clásica
(42, 5, '2026-03-01 12:00:00'),
(43, 5, '2026-03-02 13:00:00'),
(44, 5, '2026-03-03 14:00:00'),
(45, 5, '2026-03-04 15:00:00'),
(46, 5, '2026-03-05 16:00:00'),

-- Cliente 6: 20 asistencias → VIP
(47, 6, '2026-03-01 08:00:00'),
(48, 6, '2026-03-02 09:00:00'),
(49, 6, '2026-03-03 10:00:00'),
(50, 6, '2026-03-04 11:00:00'),
(51, 6, '2026-03-05 12:00:00'),
(52, 6, '2026-03-06 13:00:00'),
(53, 6, '2026-03-07 14:00:00'),
(54, 6, '2026-03-08 15:00:00'),
(55, 6, '2026-03-09 16:00:00'),
(56, 6, '2026-03-10 17:00:00'),
(57, 6, '2026-03-11 18:00:00'),
(58, 6, '2026-03-12 19:00:00'),
(59, 6, '2026-03-13 20:00:00'),
(60, 6, '2026-03-14 21:00:00'),
(61, 6, '2026-03-15 22:00:00'),
(62, 6, '2026-03-16 23:00:00'),
(63, 6, '2026-03-17 00:00:00'),
(64, 6, '2026-03-18 01:00:00'),
(65, 6, '2026-03-19 02:00:00'),
(66, 6, '2026-03-20 03:00:00');

-- Actualizar niveles VIP basados en asistencias (simulando la lógica automática)
UPDATE clientes SET Nivel_Cliente = 'VIP', Fecha_VIP = '2026-03-16 08:00:00' WHERE Id_Cliente = 2; -- 16 asistencias
UPDATE clientes SET Nivel_Cliente = 'VIP', Fecha_VIP = '2026-03-15 00:00:00' WHERE Id_Cliente = 4; -- 15 asistencias
UPDATE clientes SET Nivel_Cliente = 'VIP', Fecha_VIP = '2026-03-20 03:00:00' WHERE Id_Cliente = 6; -- 20 asistencias

COMMIT;
