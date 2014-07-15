
name := "contable" 

version := "1" 

scalaVersion := "2.10.2"

libraryDependencies  ++= Seq(
  "org.scalatest" % "scalatest_2.10" % "2.2.0" % "test",
  "org.scalanlp" % "breeze_2.10" % "0.7",
  // native libraries are not included by default. add this if you want them (as of 0.7)
  // native libraries greatly improve performance, but increase jar sizes.
  "org.scalanlp" % "breeze-natives_2.10" % "0.7"
)

resolvers ++= Seq(
            // other resolvers here
            "Sonatype Releases" at "https://oss.sonatype.org/content/repositories/releases/"
)

scalaVersion := "2.10.3"
