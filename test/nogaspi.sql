-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : db_nogaspi_test
-- Généré le : dim. 06 fév. 2022 à 17:15
-- Version du serveur : 10.6.5-MariaDB-1:10.6.5+maria~focal
-- Version de PHP : 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `nogaspi`
--

-- --------------------------------------------------------

--
-- Structure de la table `allergen`
--

CREATE TABLE `allergen` (
  `id` int(11) NOT NULL,
  `nameEN` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `nameFR` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `article`
--

CREATE TABLE `article` (
  `id` int(11) NOT NULL,
  `idProduct` int(11) NOT NULL,
  `idDonation` int(11) DEFAULT NULL,
  `expirationDate` datetime NOT NULL,
  `idFridge` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `conversation`
--

CREATE TABLE `conversation` (
  `id` int(11) NOT NULL,
  `idDonation` int(11) NOT NULL,
  `idUserDonator` int(11) NOT NULL,
  `idUserTaker` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `donation`
--

CREATE TABLE `donation` (
  `id` int(11) NOT NULL,
  `idUser` int(11) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `geoPrecision` int(20) NOT NULL,
  `startingDate` datetime NOT NULL,
  `endingDate` datetime NOT NULL,
  `idDonationCode` int(11) DEFAULT NULL,
  `archive` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `donationCode`
--

CREATE TABLE `donationCode` (
  `id` int(11) NOT NULL,
  `code` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `expirationDate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `favorite_donation`
--

CREATE TABLE `favorite_donation` (
  `id` int(11) NOT NULL,
  `idUser` int(11) NOT NULL,
  `idDonation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `fridge`
--

CREATE TABLE `fridge` (
  `id` int(11) NOT NULL,
  `idUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `message`
--

CREATE TABLE `message` (
  `id` int(11) NOT NULL,
  `idConversation` int(11) NOT NULL,
  `toDonator` tinyint(1) NOT NULL,
  `readed` tinyint(1) NOT NULL,
  `dateTime` datetime NOT NULL,
  `body` text COLLATE utf8mb3_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `opinion` text COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `brand` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `quantity` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `barcode` varchar(30) COLLATE utf8mb3_unicode_ci NOT NULL,
  `image_url` varchar(100) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ingredients` text COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `nutrimentData` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `nutriscoreData` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `idLastScanUser` int(11) NOT NULL,
  `lastScanDate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `product_allergen`
--

CREATE TABLE `product_allergen` (
  `id` int(11) NOT NULL,
  `idProduct` int(11) DEFAULT NULL,
  `idAllergen` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `rang`
--

CREATE TABLE `rang` (
  `id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `userNogaspi`
--

CREATE TABLE `userNogaspi` (
  `id` int(11) NOT NULL,
  `mail` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `password` varchar(200) COLLATE utf8mb3_unicode_ci NOT NULL,
  `pseudo` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `profilePicture` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `token` varchar(100) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `token_expiration` datetime DEFAULT NULL,
  `idRang` int(11) DEFAULT NULL,
  `points` int(11) NOT NULL DEFAULT 0,
  `regularPathLatitudeStart` float DEFAULT NULL,
  `regularPathLongitudeStart` float DEFAULT NULL,
  `regularPathLatitudeEnd` float DEFAULT NULL,
  `regularPathLongitudeEnd` float DEFAULT NULL,
  `regularPathPoints` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`regularPathPoints`)),
  `fireBaseToken` varchar(200) COLLATE utf8mb3_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `allergen`
--
ALTER TABLE `allergen`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_article_donation` (`idDonation`),
  ADD KEY `fk_article_product` (`idProduct`),
  ADD KEY `fk_article_fridge` (`idFridge`);

--
-- Index pour la table `conversation`
--
ALTER TABLE `conversation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_conversation_userDonator` (`idUserDonator`),
  ADD KEY `fk_conversation_userTaker` (`idUserTaker`),
  ADD KEY `fk_conversation_donation` (`idDonation`);

--
-- Index pour la table `donation`
--
ALTER TABLE `donation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_annonce_user` (`idUser`),
  ADD KEY `fk_donation_donationCode` (`idDonationCode`);

--
-- Index pour la table `donationCode`
--
ALTER TABLE `donationCode`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `favorite_donation`
--
ALTER TABLE `favorite_donation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idDonation` (`idDonation`),
  ADD KEY `idUser` (`idUser`);

--
-- Index pour la table `fridge`
--
ALTER TABLE `fridge`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_fridge_user` (`idUser`);

--
-- Index pour la table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_message_conversation` (`idConversation`);

--
-- Index pour la table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_article_user` (`idLastScanUser`);

--
-- Index pour la table `product_allergen`
--
ALTER TABLE `product_allergen`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idProduct` (`idProduct`),
  ADD KEY `idAllergen` (`idAllergen`);

--
-- Index pour la table `rang`
--
ALTER TABLE `rang`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `userNogaspi`
--
ALTER TABLE `userNogaspi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_rang` (`idRang`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `allergen`
--
ALTER TABLE `allergen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `article`
--
ALTER TABLE `article`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `conversation`
--
ALTER TABLE `conversation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `donation`
--
ALTER TABLE `donation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `donationCode`
--
ALTER TABLE `donationCode`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `favorite_donation`
--
ALTER TABLE `favorite_donation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `fridge`
--
ALTER TABLE `fridge`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `message`
--
ALTER TABLE `message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `product_allergen`
--
ALTER TABLE `product_allergen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `rang`
--
ALTER TABLE `rang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `userNogaspi`
--
ALTER TABLE `userNogaspi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `article`
--
ALTER TABLE `article`
  ADD CONSTRAINT `fk_article_donation` FOREIGN KEY (`idDonation`) REFERENCES `donation` (`id`),
  ADD CONSTRAINT `fk_article_fridge` FOREIGN KEY (`idFridge`) REFERENCES `fridge` (`id`),
  ADD CONSTRAINT `fk_article_product` FOREIGN KEY (`idProduct`) REFERENCES `product` (`id`);

--
-- Contraintes pour la table `conversation`
--
ALTER TABLE `conversation`
  ADD CONSTRAINT `fk_conversation_donation` FOREIGN KEY (`idDonation`) REFERENCES `donation` (`id`),
  ADD CONSTRAINT `fk_conversation_userDonator` FOREIGN KEY (`idUserDonator`) REFERENCES `userNogaspi` (`id`),
  ADD CONSTRAINT `fk_conversation_userTaker` FOREIGN KEY (`idUserTaker`) REFERENCES `userNogaspi` (`id`);

--
-- Contraintes pour la table `donation`
--
ALTER TABLE `donation`
  ADD CONSTRAINT `fk_annonce_user` FOREIGN KEY (`idUser`) REFERENCES `userNogaspi` (`id`),
  ADD CONSTRAINT `fk_donation_donationCode` FOREIGN KEY (`idDonationCode`) REFERENCES `donationCode` (`id`);

--
-- Contraintes pour la table `favorite_donation`
--
ALTER TABLE `favorite_donation`
  ADD CONSTRAINT `favorite_donation_ibfk_1` FOREIGN KEY (`idDonation`) REFERENCES `donation` (`id`),
  ADD CONSTRAINT `favorite_donation_ibfk_2` FOREIGN KEY (`idUser`) REFERENCES `userNogaspi` (`id`);

--
-- Contraintes pour la table `fridge`
--
ALTER TABLE `fridge`
  ADD CONSTRAINT `fk_fridge_user` FOREIGN KEY (`idUser`) REFERENCES `userNogaspi` (`id`);

--
-- Contraintes pour la table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `fk_message_conversation` FOREIGN KEY (`idConversation`) REFERENCES `conversation` (`id`);

--
-- Contraintes pour la table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `fk_article_user` FOREIGN KEY (`idLastScanUser`) REFERENCES `userNogaspi` (`id`);

--
-- Contraintes pour la table `product_allergen`
--
ALTER TABLE `product_allergen`
  ADD CONSTRAINT `product_allergen_ibfk_1` FOREIGN KEY (`idProduct`) REFERENCES `product` (`id`),
  ADD CONSTRAINT `product_allergen_ibfk_2` FOREIGN KEY (`idAllergen`) REFERENCES `allergen` (`id`);

--
-- Contraintes pour la table `userNogaspi`
--
ALTER TABLE `userNogaspi`
  ADD CONSTRAINT `fk_user_rang` FOREIGN KEY (`idRang`) REFERENCES `rang` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
