name := """cage"""

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  cache,
  ws,
  "org.scalatestplus.play" %% "scalatestplus-play" % "1.5.0-RC1" % Test
)

resolvers += "scalaz-bintray" at "http://dl.bintray.com/scalaz/releases"

resolvers ++= Seq(
  "Websudos releases" at "https://dl.bintray.com/websudos/oss-releases/"
)

libraryDependencies += "com.websudos" % "phantom-dsl_2.11" % "1.22.0"

libraryDependencies += "joda-time" % "joda-time" % "2.9.2"

play.sbt.PlayImport.PlayKeys.playDefaultPort := 30000
