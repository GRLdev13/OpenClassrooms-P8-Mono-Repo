
# Build the executable Spring Boot JAR.
FROM eclipse-temurin:21-jdk AS builder

WORKDIR /app

COPY gradlew .
COPY gradle ./gradle
COPY build.gradle settings.gradle ./
COPY src ./src

RUN sed -i 's/\r$//' gradlew
RUN chmod +x gradlew
RUN ./gradlew clean bootJar --no-daemon

# Create the runtime image. The application starts when Compose launches the
# container, not while Docker is building the image.
FROM eclipse-temurin:21-jre

WORKDIR /app

COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
