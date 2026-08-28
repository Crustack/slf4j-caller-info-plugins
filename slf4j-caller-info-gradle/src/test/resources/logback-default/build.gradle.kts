plugins {
    java
    id("io.github.crustack.slf4j-caller-info") version "1.2.1"
}

group = "io.github.crustack"
version = "1.2.1"

java {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
    implementation("ch.qos.logback:logback-classic:1.2.6")

    testImplementation("junit:junit:4.13.2")
}