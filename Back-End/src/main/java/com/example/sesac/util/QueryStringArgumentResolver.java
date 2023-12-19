package com.example.sesac.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.core.MethodParameter;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.support.WebDataBinderFactory;
import org.springframework.web.context.request.NativeWebRequest;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.method.support.ModelAndViewContainer;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

@Component
@RequiredArgsConstructor
public class QueryStringArgumentResolver implements HandlerMethodArgumentResolver {
    private final ObjectMapper om;

    @Override
    public boolean supportsParameter(final MethodParameter methodParameter) {
        return methodParameter.getParameterAnnotation(QueryStringArgResolver.class) != null;
    }

    @Override
    public Object resolveArgument(final MethodParameter methodParameter,
                                  final ModelAndViewContainer modelAndViewContainer,
                                  final NativeWebRequest nativeWebRequest,
                                  final WebDataBinderFactory webDataBinderFactory) throws Exception {
        final HttpServletRequest request = (HttpServletRequest) nativeWebRequest.getNativeRequest();
        final String json = queryToJson(URLDecoder.decode(request.getQueryString(), StandardCharsets.UTF_8));
        return om.readValue(json, methodParameter.getParameterType());
    }

    private String queryToJson(String query) {
        StringBuilder result = new StringBuilder("{\"");
        for (int i = 0; i < query.length(); i++) {
            if (query.charAt(i) == '=') {
                result.append("\"" + ":" + "\"");
            } else if (query.charAt(i) == '&') {
                result.append("\"" + "," + "\"");
            } else {
                result.append(query.charAt(i));
            }
        }
        result.append("\"" + "}");
        return result.toString();
    }
}